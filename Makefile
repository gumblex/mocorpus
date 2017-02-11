A2_MAXNUM=8
A2_MAXCONPERSRV=10
A2_SPLITCON=8
A2_MINSPLITSZ=1M

.PHONY: clean prunedebs

mocorpus.db: locale/.done
	python3 readmo.py mocorpus.db locale/

packages.txt:
	apt-file search -x 'usr/share/locale/.+/LC_MESSAGES/.+\.mo' \
		| cut -d: -f 1 \
		| uniq \
		| parallel --xargs apt-get download -y --print-uris \
		| awk -f apt2aria.awk > packages.txt

debs/.done: packages.txt
	mkdir -p debs && \
	cd debs && \
	aria2c -c -j $(A2_MAXNUM) -x $(A2_MAXCONPERSRV) -s $(A2_SPLITCON) \
		-i ../packages.txt --min-split-size=$(A2_MINSPLITSZ) --connect-timeout=600 \
		--timeout=600 -m0 --conditional-get=true --auto-file-renaming=false && \
	touch .done

locale/.done: debs/.done | prunedebs
	find debs/ -type f -name '*.deb' | \
		parallel 'dpkg --fsys-tarfile {} | \
			tar xf - --strip-components=3 ./usr/share/locale' && \
	touch locale/.done

prunedebs:
	find debs/ -type f -name '*.deb' | \
		sort -t _ -k 1,1 -k 2Vr | \
		awk 'BEGIN {FS = "_"; last = "";} {if ($$1 == last) print; last = $$1;}' | \
		xargs -r rm

clean:
	rm -rf packages.txt debs/ locale/
