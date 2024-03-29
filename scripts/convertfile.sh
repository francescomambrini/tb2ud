#!/usr/bin/env bash

# NOTE 1: we use a LOCAL version of createupos and createfeats

# NOTE 2: In the future, I should use the new TransformArtificials,
# instead of the old SetArtificials

# Note 3: I now use the Udapi_AGLDT package; all else is now local

# TODO: update createupos and createfeats when they're stable

# Left .RehangPunct out between FixObj and tb2ud.deprecated.SetArtificials

# set the pipeline straight
#udapy .udapi_agldt.read.Glaux files="$1" fix_cycles=True\
udapy -v .udapi_agldt.read.Agldt files="$1" fix_cycles=True\
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
  util.Eval doc='doc.meta["docname"]=doc.meta["loaded_from"][:-4]+".conllu"' \
  write.Conllu docname_as_file=1
