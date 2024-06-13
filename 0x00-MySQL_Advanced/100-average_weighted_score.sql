-- Create the procedure ComputeAverageWeightedScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE weighted_score FLOAT;
    
    -- Calculate the weighted average score for the given user
    SET weighted_score = (
        SELECT SUM(c.score * p.weight) / SUM(p.weight)
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id
    );
    
    -- Update the average_score field in the users table
    UPDATE users
    SET average_score = weighted_score
    WHERE id = user_id;
    
END//

DELIMITER ;
