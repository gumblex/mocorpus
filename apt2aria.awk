#!/usr/bin/awk -f
BEGIN {
    FS = " ";
}
{
    gsub(/^'|'$/, "", $1);
    split($4, chksum, ":");
    print $1;
    if (chksum[1] == "SHA256") {
        chksumtype = "sha-256";
    } else if (chksum[1] == "SHA1") {
        chksumtype = "sha-1";
    } else if (chksum[1] == "MD5Sum") {
        chksumtype = "md5";
    } else {
        chksumtype = "";
    }
    if (chksumtype != "") {
        printf(" checksum=%s=%s\n", chksumtype, chksum[2]);
    }
    printf(" out=%s\n", $2);
}
