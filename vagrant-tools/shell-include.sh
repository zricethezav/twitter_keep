
# load up configs into env variables
IFS="="
while read -r name value
do
    export $name=$value
done < /home/vagrant/twitter_keep/.twitter
