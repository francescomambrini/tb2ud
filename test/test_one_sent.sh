#!/usr/bin/env bash

udapy read.Agldt files="data/testsent1.xml" \
    agldt.SetSpaceAfter \
    agldt.CreateUpos   \
    agldt.CreateFeats   \
    .SetMember   \
    .ShallowConverter   \
    .SubTreeConverter with_enhanced="True" \
    write.Conllu files="data/testonesent.conllu"
