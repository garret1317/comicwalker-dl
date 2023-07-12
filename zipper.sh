#!/bin/sh
for i in */
do zip "${i%*/}.cbz" -r "$i"
done
