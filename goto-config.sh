#!/bin/bash

#Specify parent directories where the gogo scripts fetches data from
#GOTO_PARENT_DIRECTORIES=(~/Projects)
#Specify prefixes to exclude from names
#GOTO_REMOVE_PREFIXES=("zeos-" "zalando-")

function remove_prefix() {
  result=$1
  for remove_prefix in ${GOTO_REMOVE_PREFIXES[*]}; do
    result=${result#$remove_prefix}
  done
  echo $result
}

for parent_dir in ${GOTO_PARENT_DIRECTORIES[*]}; do

  for goto_dir_name in $( ls $parent_dir ); do
  
    goto_full_path="$parent_dir/$goto_dir_name"
    
    if [[ -d $goto_full_path ]]; then
      goto_target=$( remove_prefix $goto_dir_name )
      alias goto-$goto_target="cd $goto_full_path"
    fi
  done
done
