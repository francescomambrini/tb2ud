#!/usr/bin/env bash

# NOTE 1: we use a LOCAL version of createupos and createfeats

# NOTE 2: I now use the new TransformArtificials, instead of the old SetArtificials, for testing purposes

# TODO: update createupos and createfeats when they're stable


# set the pipeline straight
udapy read.Agldt files="$1" \
  agldt.SetSpaceAfter \
  .CreateUpos \
  .CreateFeats \
  .SetMember \
  .ShallowConverter \
  .ShiftArtificials \
  .SubTreeConverter with_enhanced="True" \
  .FixObj \
  .RehangPunct \
  .TransformArtificials \
  .MakeEnhanced \
  .postprocess.FixSomePos \
  .PurgeMisc \
  .text.UpdateText \
  util.Eval doc='doc.meta["docname"]=doc.meta["loaded_from"][:-4]+"_TRANSFORM.conllu"' \
  write.Conllu docname_as_file=1
