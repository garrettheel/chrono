# Populate some artificial metrics so we have data to work with


function populate {
    for i in `seq 1 10`;
    do
      for _ in `seq 1 50`;
      do
        echo -n "${1}.${i}.p90:$(echo "scale=2; $(echo $RANDOM)/10000" | bc -l)|g" | nc -w 1 -u $(docker-machine ip default) 8125;
      done
    done
}

populate "service.web.duration"
