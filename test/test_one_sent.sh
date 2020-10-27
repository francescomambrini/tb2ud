#!/usr/bin/env bash

udapy read.Agldt files="test/data/testsent1.xml" \
    agldt.SetSpaceAfter \
    agldt.CreateUpos   \
    agldt.CreateFeats   \
    .SetMember   \
    .ShallowConverter   \
    .SubTreeConverter \
    write.Conllu files="test/data/testonesent.conllu"
