-- A script for a stored procedure that computes and store the average score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)
BEGIN
	DECLARE total_score FLOAT DEFAULT 0;
	DECLARE total_projects INT DEFAULT 0;
	SELECT SUM(score), COUNT(*) INTO total_score, total_projects
	FROM corrections WHERE corrections.user_id = user_id;

	UPDATE users
	SET users.average_score = total_score / total_projects
	WHERE users.id = user_id;
END //
DELIMITER ;
