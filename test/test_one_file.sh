#!/usr/bin/env bash

udapy read.Agldt files="$1" \
    agldt.SetSpaceAfter \
    agldt.CreateUpos   \
    agldt.CreateFeats   \
    .RemoveArts \
    .SetMember   \
    .ShallowConverter   \
    .SubTreeConverter \
    write.Conllu files="test/data/testafile.conllu"
