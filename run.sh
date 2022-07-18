#####################################################################
# run.sh                                                            #
# run this script to turn on the clock                              #
# Later, this command will feature more args and customizations for #
# running the clock. For now, this is just boilerplate code.        #
#                                                                   #
# Jack Donofrio                                                     #
#####################################################################

echo Starting up clock...
python3 alarm.py

# clean up logfile - sometimes the same error gets repeated many times in a row; this
# makes it so consecutively repeating lines get condensed with a parenthesized count next to them
if [[ -f alarm.log ]]; then
  echo "$(uniq -c alarm.log | awk '{ if ($1 != "1") {$(NF + 1) = "("$1")"}; $1 = ""} sub(FS, "")')" > alarm.log
fi
