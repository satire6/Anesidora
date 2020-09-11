#!/bin/sh
DOW=`date +%A` 
#DOW='Thursday'
echo "$DOW"
#Move to the location where you want to run the script
cd /event_logs/
rm /event_logs/toon*.gz
scp toonpub@toon21:/log/live/event/`date -d yesterday +%Y/%m/%d`/* .
#scp toonpub@toon21:/log/live/event/2005/12/14/* .
#Searches the file for completed quests
rm ttoon_*
zgrep -h  '|questComplete|' /event_logs/toon*.gz 	| awk -F \| '{print $4}'> ttoon_quest
zgrep -h  '|buildingDefeated|' /event_logs/toon*.gz 	| awk -F \| '{print $4}'> ttoon_building_defeated
zgrep -h  '|fishedFish|' /event_logs/toon*.gz 		| awk -F \| '{print $4}' > ttoon_fish
zgrep -h  '|fishedBoot|' /event_logs/toon*.gz 		| awk -F \| '{print $4}' > ttoon_boot
zgrep -h  '|catalog-purchase|' /event_logs/toon*.gz 	| awk -F \| '{print $4}' > ttoon_catalogs
zgrep -h  '|minigame|' /event_logs/toon*.gz 		| awk -F \| '{print $4}' > ttoon_minigame
zgrep -h  '|kartingPlaced|' /event_logs/toon*.gz  	| awk -F \| '{print $4"|"$5}' | grep "|1" | awk -F \| '{print $1}' > ttoon_karting_placed
zgrep -h  '|minigame|' /event_logs/toon*.gz 		| awk -F \| '{print $4"\t"$8}' > ttoon_beans
zgrep -h  '|fishedFish|' /event_logs/toon*.gz 		| awk -F \| '{print $4"\t"$10}' >> ttoon_beans
zgrep -h  '|kartingTicketsSpent|' /event_logs/toon*.gz 	| awk -F \| '{print $4"\t"$5}' > ttoon_tickets_spent
zgrep -h '|merits|' /event_logs/toon*.gz 		| awk -F \| '{print $4"\t"$8}' > ttoon_merits
zgrep -h '|merits|' /event_logs/toon*.gz 		| awk -F \| '{print $4"\t"$7}' > ttoon_bucks
zgrep -h  '|bossBattle|' /event_logs/toon*.gz 		| grep "|s|" | grep "|Victory|" | awk -F \| '{print $7}' | sed -e 's/\[//g' -e 's/]//g' -e 's/,/\n/g' -e 's/ //g' -e 's/L//g' > ttoon_VP
zgrep -h  '|bossBattle|' /event_logs/toon*.gz 		| grep "|m|" | grep "|Victory|" | awk -F \| '{print $7}' | sed -e 's/\[//g' -e 's/]//g' -e 's/,/\n/g' -e 's/ //g' -e 's/L//g' > ttoon_cfo_victory
zgrep -h  '|cogsDefeated|' /event_logs/toon*.gz | awk -F \| '{print $4"|"$5}' | sed -e 's/+//g' -e 's/10$//g'  -e 's/11$//g'  -e 's/12$//g' -e 's/10,/,/g'  -e 's/11,/,/g'  -e 's/12,/,/g' -e 's/[0-9],/,/g' -e 's/[0-9]$//g' -e 's/[a-z]//g'| awk -F \| '{print $1","$2}' | awk -F \, '{s=0;for (i=1; i<=NF; i++) s=(s+$i); print $1"\t"s-$1}' > ttoon_cogs_defeated
if [ $DOW = "Thursday" ]
then
echo "$DOW"
zgrep -i "fishbingowin"  /event_logs/toon*.gz | awk -F \| '{print $8"\n"$9"\n"$10"\n"$11}' > ttoon_bingo_win
awk -f /home/toonpub/scripts/word_freq.awk ttoon_bingo_win              | sort +1 -nr   |  sed 5q       > top_fish_bingo
else
echo "Not Thursday move on"
fi

awk -f /home/toonpub/scripts/word_freq.awk ttoon_quest 			| sort +1 -nr 	|  sed 5q 	> top_quests		
awk -f /home/toonpub/scripts/word_freq.awk ttoon_building_defeated 	| sort +1 -nr	|  sed 5q	> top_buildings
awk -f /home/toonpub/scripts/word_freq.awk ttoon_fish 			| sort +1 -nr	|  sed 5q 	> top_fish
awk -f /home/toonpub/scripts/word_freq.awk ttoon_boot 			| sort +1 -nr	|  sed 5q	> top_boot
awk -f /home/toonpub/scripts/word_freq.awk ttoon_catalogs 		| sort +1 -nr	|  sed 5q	> top_catalogs
awk -f /home/toonpub/scripts/word_freq.awk ttoon_minigame 		| sort +1 -nr	|  sed 5q 	> top_minigame
awk -f /home/toonpub/scripts/word_freq.awk ttoon_karting_placed 	| sort +1 -nr	|  sed 5q	> top_karting_placed
awk -f /home/toonpub/scripts/word_freq.awk ttoon_VP 			| sort +1 -nr	|  sed 5q	> top_VP
awk -f /home/toonpub/scripts/word_freq.awk ttoon_cfo_victory 		| sort +1 -nr	|  sed 5q	> top_CFO
awk '{ x[$1] += $2 } END { for ( i in x ) print i, x[i] }' < ttoon_merits 		|  sort +1 -nr |  sed 5q > top_merits
awk '{ x[$1] += $2 } END { for ( i in x ) print i, x[i] }' < ttoon_bucks  		|  sort +1 -nr |  sed 5q > top_bucks
awk '{ x[$1] += $2 } END { for ( i in x ) print i, x[i] }' < ttoon_beans  		|  sort +1 -nr |  sed 5q > top_beans
awk '{ x[$1] += $2 } END { for ( i in x ) print i, x[i] }' < ttoon_tickets_spent  	|  sort +1 -nr |  sed 5q > top_tickets
awk '{ x[$1] += $2 } END { for ( i in x ) print i, x[i] }' < ttoon_cogs_defeated 	|  sort +1 -nr |  sed 5q > top_cogs
cd /event_logs/
rm /event_logs/top_toons
rm /game_logs/topToonPictures/TopToons.txt
mkdir /event_logs/topToonImages/`date -d yesterday +%Y_%m_%d`
mkdir /event_logs/topToonImages/`date -d yesterday +%Y_%m_%d_small`

cat top_cogs 		>> /event_logs/top_toons
cat top_buildings 	>> /event_logs/top_toons
cat top_catalogs 	>> /event_logs/top_toons
cat top_quests 		>> /event_logs/top_toons
cat top_minigame 	>> /event_logs/top_toons
cat top_beans 		>> /event_logs/top_toons
cat top_fish 		>> /event_logs/top_toons
cat top_boot 		>> /event_logs/top_toons
cat top_merits 		>> /event_logs/top_toons
cat top_VP 		>> /event_logs/top_toons
cat top_bucks 		>> /event_logs/top_toons
cat top_CFO 		>> /event_logs/top_toons
cat top_karting_placed 	>> /event_logs/top_toons
cat top_tickets 	>> /event_logs/top_toons
if [ $DOW  = "Thursday" ]
then
echo "$DOWN"
cat top_fish_bingo      >>  /event_logs/top_toons
else
echo "Not Thursday move on"
fi

cd /event_logs/
cat /event_logs/top_toons | sed -n '1~5p' | awk -F \  '{print $1}' > /event_logs/toon_images
rm /event_logs/dna
rm /event_logs/top_toon_dna

for file in $(cat /event_logs/toon_images);
	do
	wget --http-user=a1rw0lf --http-passwd=str33th4wk http://10.192.44.249:7780/_do_querry___data_toontown_dat?object_id=$file -O /event_logs/dna 
	cat /event_logs/dna | sed -e 's/<\/TH>/<\/TH>\n/g' | grep -a "setDNA" -A 1 | awk -F \< '{print $5}' | sed '2q' |awk -F \> '{print $1}' >> /event_logs/top_toon_dna
	done
cat /event_logs/top_toon_dna | sed '/^$/d' > /game_logs/topToonPictures/TopToons.txt
cat /game_logs/topToonPictures/TopToons.txt | awk -F \\n '{print$1".jpg"}'|sed 1,1's/^/topToonImages=/g' > /event_logs/topToonImages/`date -d yesterday +%Y_%m_%d_small`/TopToonImages.txt
cat /event_logs/top_toons | awk -F \  '{print $1}' > /event_logs/toon_names
rm /event_logs/names
rm /event_logs/top_toon_names
rm /event_logs/top_toon_score_nav
for file in $(cat /event_logs/toon_names);
	do
	wget --http-user=a1rw0lf --http-passwd=str33th4wk http://10.192.44.249:7780/_do_querry___data_toontown_dat?object_id=$file -O /event_logs/names
	grep -a "name='new_name" /event_logs/names | sed -e 's/<input type=text value=//g' | awk -F \' '{print $2}' >> /event_logs/top_toon_names
	done 

cat /event_logs/top_toon_names |sed 1,1's/^/topToons=/g'|sed 50's/$/\&/' > /event_logs/topToonImages/`date -d yesterday +%Y_%m_%d_small`/TopToons.txt
cat /event_logs/topToonImages/`date -d yesterday +%Y_%m_%d_small`/TopToons.txt >> /event_logs/topToonImages/`date -d yesterday +%Y_%m_%d_small`/TopToon.txt
rm /event_logs/toon_scores
cat /event_logs/top_toons | awk -F \  '{print $2}' > /event_logs/toon_scores
cat /event_logs/top_toons | awk -F \  '{print $2}' >> /event_logs/topToonImages/`date -d yesterday +%Y_%m_%d_small`/TopToon.txt 
cat /event_logs/toon_scores | sed 1,1's/^/\&topToonScores=/g' > /event_logs/top_toon_score_nav
cat /event_logs/top_toon_score_nav >> /event_logs/topToonImages/`date -d yesterday +%Y_%m_%d_small`/TopToon.txt

cd /game_logs/topToonPictures/
cp /game_logs/topToonPictures2/ttp.prc /game_logs/topToonPictures/ttp.prc
cat ttp.prc | sed 's/win-width 50/win-width 60/g' | sed 's/win-height 50/win-height 60/g' > temp_log | mv temp_log ttp.prc
./runTTP.sh
cat ttp.prc | sed 's/win-width 60/win-width 50/g' | sed 's/win-height 60/win-height 50/g' > temp_log | mv temp_log ttp.prc
./runTTP_yellow.sh

if [ $DOW = "Thursday" ]
then
echo "$DOW"
echo "USED THURSDAY PHP"
php -q /vol01/www/html/topToonsphppageRacingThursday.php > /event_logs/`date -d yesterday +%Y_%m_%d`.php
cat /event_logs/`date -d yesterday +%Y_%m_%d`.php | sed 's/Content-type: text\/html//' > /event_logs/topToons_`date -d yesterday +%Y_%m_%d`.php
else
echo "non Thursday"
php -q /vol01/www/html/topToonsphppageRacing.php > /event_logs/`date -d yesterday +%Y_%m_%d`.php
cat /event_logs/`date -d yesterday +%Y_%m_%d`.php | sed 's/Content-type: text\/html//' > /event_logs/topToons_`date -d yesterday +%Y_%m_%d`.php
fi
echo "created php pages"
scp /event_logs/topToons_`date -d yesterday +%Y_%m_%d`.php toonpub@toon21:/toontown/1400/common/dynamic/topToons/
scp -r /event_logs/topToonImages/`date -d yesterday +%Y_%m_%d`/ toonpub@toon21:/toontown/1400/common/shared/images/dynamic/topToonImages/
scp -r /event_logs/topToonImages/`date -d yesterday +%Y_%m_%d_small`/ toonpub@toon21:/toontown/1400/common/shared/images/dynamic/topToonImages/
echo "Moved Images to 21"
top_toon_file_count=`wc -l /event_logs/topToonImages/`date -d yesterday +%Y_%m_%d_small`/TopToon.txt`

#ssh toonpub@toon21 /home/toonpub/bin/syncTopToons.sh live
ssh toonpub@toon21 /home/toonpub/bin/syncTopToons.sh qa

#mysql -u rweiner -pmini100 remarks_orig_copy < top_toon_images > top_toon_dna
