#!/usr/bin/env bash

# NOTE: we use a LOCAL version of createupos and createfeats


# set the pipeline straight
udapy -v .udapi_agldt.read.Glaux fix_cycles=True files=@input.fl \
  .SetSpaceAfter \
  .CreateUpos \
  .CreateFeats \
  .SetMember \
  .ShallowConverter \
  .udapi_agldt.util.ShiftArtificials \
  .SubTreeConverter with_enhanced="True" \
  .FixObj \
  .RehangPunct \
  .tb2ud.deprecated.SetArtificials \
  .MakeEnhanced \
  .postprocess.FixSomePos \
  .PurgeMisc \
  .text.UpdateText \
  write.Conllu files=@output.fl
