-- Create the procedure ComputeAverageWeightedScoreForUsers
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id INT;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Calculate the weighted average score for the current user
        UPDATE users u
        SET u.average_score = (
            SELECT SUM(c.score * p.weight) / SUM(p.weight)
            FROM corrections c
            JOIN projects p ON c.project_id = p.id
            WHERE c.user_id = u.id
        )
        WHERE u.id = user_id;
        
    END LOOP;
    
    CLOSE cur;
END;

//

DELIMITER ;
