# Example of SQL query
query_example = """
                SELECT mascot
                FROM `bigquery-public-data.ncaa_basketball.mascots` 
                WHERE market = 'Georgia Tech'
                """

#### YOUR CODE GOES BELOW HERE  #####

#(1)
query_1 = """ 
          (SELECT DISTINCT P.id, P.name
          FROM `cs4400_ncaa_basketball.game` as G, `cs4400_ncaa_basketball.player_game` as PG, `cs4400_ncaa_basketball.player` as P
          WHERE (G.season = 2013 and G.id = PG.game_id and PG.player_id = P.id)
          ORDER BY P.name)

          INTERSECT DISTINCT 

          (SELECT DISTINCT P.id, P.name
          FROM `cs4400_ncaa_basketball.game` as G, `cs4400_ncaa_basketball.player_game` as PG, `cs4400_ncaa_basketball.player` as P
          WHERE (G.season = 2017 and G.id = PG.game_id and PG.player_id = P.id)
          ORDER BY P.name)

          ORDER BY name
          """

#(2)
query_2 = """ 
          SELECT DISTINCT PG.player_id as id, P.name
          FROM `cs4400_ncaa_basketball.player` as P, `cs4400_ncaa_basketball.player_game` as PG, `cs4400_ncaa_basketball.game` as G
          WHERE PG.player_id = P.id and PG.game_id = G.id
          group by P.name, PG.player_id, G.season
          HAVING count(*) >= 40
          ORDER by P.name 
          """

#(3)
query_3 = """ 
          (SELECT P.id, P.name
          FROM `cs4400_ncaa_basketball.player_game` as PG JOIN `cs4400_ncaa_basketball.player` as P ON P.id = PG.player_id
          WHERE PG.points IS NOT NULL AND PG.points > 10
          GROUP BY P.id, P.name
          HAVING COUNT(PG.game_id) > 10)

          EXCEPT DISTINCT

          (SELECT P.id, P.name
          FROM `cs4400_ncaa_basketball.player_game` as PG JOIN `cs4400_ncaa_basketball.player` as P ON P.id = PG.player_id
          WHERE PG.points IS NOT NULL AND PG.points < 10
          GROUP BY P.id, P.name)

          ORDER BY name
          """

#(4)
query_4 = """ 
          SELECT DISTINCT P.id, P.name
          FROM `cs4400_ncaa_basketball.player` as P join `cs4400_ncaa_basketball.player_game` as PG on P.id = PG.player_id 
            join `cs4400_ncaa_basketball.team_game` as TG on TG.game_id = PG.game_id
            join `cs4400_ncaa_basketball.team` as T on TG.h_id = T.id,
            `cs4400_ncaa_basketball.venue` as V
          WHERE PG.points IS NOT NULL and P.birthplace_city = V.venue_city and T.venue_id = V.id
          ORDER BY P.name 
          """

#(5)
query_5 = """ 
          SELECT DISTINCT 
            CASE WHEN A.player_id < B.player_id THEN A.player_id
            ELSE B.player_id END AS player1_id,
            CASE WHEN A.player_id < B.player_id THEN B.player_id
            ELSE A.player_id END AS player2_id,
          ROUND(AVG(A.points + B.points), 2) as average_partner_points
          FROM (
            (SELECT *
            FROM `cs4400_ncaa_basketball.player` as P1 join `cs4400_ncaa_basketball.player_game` as PG1 on P1.id = PG1.player_id
            WHERE PG1.points IS NOT NULL) as A join
            (SELECT *
            FROM `cs4400_ncaa_basketball.player` as P2 join `cs4400_ncaa_basketball.player_game` as PG2 on P2.id = PG2.player_id
            WHERE PG2.points IS NOT NULL) as B on A.game_id = B.game_id and A.player_id <> B.player_id)
          GROUP BY player1_id, player2_id
          HAVING COUNT(*) > 30 AND AVG(A.points + B.points) > 40
          ORDER BY average_partner_points desc
          """

#(6)
query_6 = """ 
          SELECT T.name as team_name, T.school, T.color
          FROM `cs4400_ncaa_basketball.team` as T
          WHERE T.color LIKE '#ff____' OR T.color LIKE '#FF____'
          ORDER BY T.name
          """

#(7)
query_7 = """ 
          SELECT SUM(CASE WHEN TG.h_points-TG.a_points>0 then 1 else 0 end) as num_win,
            SUM(CASE WHEN TG.h_points-TG.a_points<0 then 1 else 0 end) as num_lose 
          FROM `cs4400_ncaa_basketball.team` as T join `cs4400_ncaa_basketball.team_game` as TG on T.id = TG.h_id
            join `cs4400_ncaa_basketball.game` as G on G.id = TG.game_id
          WHERE T.school = 'Georgia Tech' and G.season = 2017
          """

#(8)
query_8 = """ 
          SELECT T.name as win_team_name, T2.name as lose_team_name, win_team_points, lose_team_points, win_margin
          FROM
              ((SELECT DISTINCT
                CASE WHEN TG.h_points-TG.a_points > 0 THEN TG.h_id
                ELSE TG.a_id
                END AS win_team_name,

                CASE WHEN TG.h_points-TG.a_points > 0 THEN TG.a_id
                ELSE TG.h_id
                END AS lose_team_name,

                CASE WHEN TG.h_points-TG.a_points > 0 THEN TG.h_points
                ELSE TG.a_points
                END AS win_team_points,

                CASE WHEN TG.h_points-TG.a_points > 0 THEN TG.a_points
                ELSE TG.h_points
                END AS lose_team_points,

                CASE WHEN TG.h_points-TG.a_points > 0 THEN TG.h_points-TG.a_points
                ELSE TG.a_points-TG.h_points
                END AS win_margin
                FROM `cs4400_ncaa_basketball.team` as T join `cs4400_ncaa_basketball.team_game` as TG on T.id = TG.h_id
                ORDER BY win_margin desc, win_team_points desc) as A 
                  join `cs4400_ncaa_basketball.team` AS T on T.id = A.win_team_name
                  join `cs4400_ncaa_basketball.team` AS T2 on T2.id = A.lose_team_name)
            ORDER BY win_margin desc, win_team_points desc LIMIT 10

          """

#(9)
query_9 = """ 
          (SELECT DISTINCT T.name as team_name, T.school
          FROM `cs4400_ncaa_basketball.team` as T join `cs4400_ncaa_basketball.team_game` as TG on T.id = TG.a_id or T.id = TG.h_id
            join `cs4400_ncaa_basketball.player_game` as PG on TG.game_id = PG.game_id and T.id = PG.team_id
            join `cs4400_ncaa_basketball.player` as P on P.id = PG.player_id,
            `cs4400_ncaa_basketball.game` as G
          WHERE G.season = 2017 and PG.points IS NOT NULL and PG.points > 0
          GROUP BY T.name, T.school, P.id)

          EXCEPT DISTINCT 

          (SELECT DISTINCT T.name as team_name, T.school
          FROM `cs4400_ncaa_basketball.team` as T join `cs4400_ncaa_basketball.team_game` as TG on T.id = TG.a_id or T.id = TG.h_id
            join `cs4400_ncaa_basketball.player_game` as PG on TG.game_id = PG.game_id and T.id = PG.team_id
            join `cs4400_ncaa_basketball.player` as P on P.id = PG.player_id,
            `cs4400_ncaa_basketball.game` as G
          WHERE G.season = 2017
          GROUP BY T.name, T.school, P.id
          HAVING SUM(PG.points) = 0)

          ORDER BY team_name
          """

#(10)
query_10 = """ 
          SELECT DISTINCT T.name AS team_name, T.school
          FROM `cs4400_ncaa_basketball.team` AS T JOIN `cs4400_ncaa_basketball.team_game` AS TG ON T.id = TG.h_id OR T.id = TG.a_id
            JOIN `cs4400_ncaa_basketball.game` AS G ON G.id = TG.game_id
            JOIN (
                    SELECT T1.name AS team_name, T1.school, COUNT(*) AS wins
                    FROM `cs4400_ncaa_basketball.team` AS T1 JOIN `cs4400_ncaa_basketball.team_game` AS TG1 on T1.id = TG1.h_id OR T1.id = TG1.a_id
                      JOIN `cs4400_ncaa_basketball.game` AS G1 on G1.id = TG1.game_id
                    WHERE G1.season = 2017 AND ((T1.id = TG1.h_id AND TG1.h_points > TG1.a_points) OR (T1.id = TG1.a_id AND TG1.h_points < TG1.a_points))
                    GROUP BY T1.name, T1.school
                    ORDER BY wins DESC) AS W on W.school = T.school  AND T.name = W.team_name
          WHERE wins = (SELECT MAX(wins) 
                        FROM (SELECT T1.name AS team_name, T1.school, COUNT(*) AS wins
                              FROM `cs4400_ncaa_basketball.team` AS T1 JOIN `cs4400_ncaa_basketball.team_game` AS TG1 ON T1.id = TG1.h_id OR T1.id = TG1.a_id
                                JOIN `cs4400_ncaa_basketball.game` AS G1 ON G1.id = TG1.game_id
                              WHERE G1.season = 2017 AND ((T1.id = TG1.h_id AND TG1.h_points > TG1.a_points) OR (T1.id = TG1.a_id AND TG1.h_points < TG1.a_points))
                              GROUP BY T1.name, T1.school))
           """

#### YOUR CODE GOES ABOVE HERE  #####