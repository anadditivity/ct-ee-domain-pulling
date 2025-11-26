#!/bin/bash
find ./all-certificates/ -type f -exec sha256sum {} + | awk '{print $1 "\t" $2}' | sort | uniq -w64 -D | sort -k1,1 | awk '
    {
    if (prev == $1) {
        printf "%s %s\n", prev_file, $2;
        printf "%s %s\n", $2, prev_file;
    }
        prev = $1;
        prev_file = $2;
    }
' | sort -u > detected-duplicate-certs.txt

# possible alternative find . -type f -exec sha256sum {} + | sort | uniq -w64 -d
# can remove with `xargs -a python-duplicate-certificates.txt rm --`