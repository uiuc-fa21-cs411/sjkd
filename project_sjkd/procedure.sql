create procedure generate_playlist_concerts(
    IN src INT, IN dest INT, IN select_flag VARCHAR(10), IN today VARCHAR(15), 
    OUT playlist_time INT, OUT trip_time INT) 
begin 
    declare finished INT default 0; 
    declare last_songID INT; 
    declare song_id INT; 
    declare duration REAL; 

    declare src_cursor CURSOR for 
        select SongID, Song.Duration 
        from Song inner join City on Song.CityID = City.CityID 
        where City.CityID = src 
        order by SongID; 
    declare dest_cursor CURSOR for 
        select SongID, Song.Duration 
        from Song inner join City on Song.CityID = City.CityID 
        where City.CityID = dest 
        order by SongID; 
    declare CONTINUE HANDLER FOR NOT FOUND SET finished = 1; 

    set playlist_time = 0; 
    set trip_time = 0; 
    if (select_flag = "playlist") then 
        select TravelTime_min 
        into trip_time 
        from Route 
        where (StartCityID = src and EndCityID = dest) 
            or (StartCityID = dest and EndCityID = src); 

        open src_cursor; 
        fetch next from src_cursor into song_id,duration; 
        repeat 
            if playlist_time < trip_time / 2 then 
                set playlist_time = playlist_time + (duration / 60 + 1); 
                set last_songID = song_id; 
            elseif playlist_time >= trip_time / 2 then set playlist_time = playlist_time;
            end if; 
            fetch next from src_cursor into song_id,duration; 
        until finished 
        end repeat; 
        close src_cursor; 
        set finished = 0; 

        select SongName, ArtistName, Song.Duration, CityName 
        from Song inner join City on Song.CityID = City.CityID 
        where City.CityID = src and Song.SongID <= last_songID 
        order by SongID; 

        open dest_cursor; 
        fetch next from dest_cursor into song_id,duration; 
        repeat 
            if playlist_time < trip_time then 
                set playlist_time = playlist_time + (duration / 60 + 1); 
                set last_songID = song_id; 
            elseif playlist_time >= trip_time then set playlist_time = playlist_time;
            end if; 
            fetch next from dest_cursor into song_id,duration; 
        until finished 
        end repeat; 
        close dest_cursor; 

        select SongName, ArtistName, Song.Duration, CityName 
        from Song inner join City on Song.CityID = City.CityID 
        where City.CityID = dest and Song.SongID <= last_songID 
        order by SongID; 
    else 
        select Date, Time, ConcertName, Location 
        from Concert 
        where Date >= today and CityID = dest 
        order by ConcertID 
        limit 5; 
    end if; 
end