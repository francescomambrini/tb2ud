#!/usr/bin/env bash

# NOTE: we use a LOCAL version of createupos and createfeats


# set the pipeline straight
udapy read.Agldt files=@input.fl \
  agldt.SetSpaceAfter \
  .CreateUpos \
  .CreateFeats \
  .SetMember \
  .ShallowConverter \
  .ShiftArtificials \
  .SubTreeConverter with_enhanced="True" \
  .FixObj \
  .RehangPunct \
  .SetArtificials \
  .postprocess.RemoveEmpty \
  .postprocess.FixSomePos \
  .PurgeMisc \
  .text.UpdateText \
  write.Conllu files=@output.fl
