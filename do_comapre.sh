#!/usr/bin/bash
set -u

new=`git reflog show blank_allowed |head -n 1 |awk '{print $1}'`
old=`git reflog show blank_allowed |tail -n 1 |awk '{print $1}'`

echo "create compare $new $old"

diff_dir="diff_dir"
new_dir=$diff_dir/"new"_$new
old_dir=$diff_dir/"old"_$old


[ -d $new_dir ] || mkdir -p $new_dir && echo "mkdir $new_dir"
[ -d $old_dir ] || mkdir -p $old_dir && echo "mkdir $old_dir"

rm $new_dir/* -rf
rm $old_dir/* -rf

old_files=`git diff --diff-filter=a --name-only $old $new`
new_files=`git diff --name-only $old $new`


git archive --format=tar $new $new_files |tar -x -C $new_dir
git archive --format=tar  $old $old_files |tar -x -C $old_dir
