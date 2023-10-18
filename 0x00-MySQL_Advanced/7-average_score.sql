-- A script for a stored procedure that computes and store the average score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)
BEGIN
	DECLARE total_score FLOAT;
	DECLARE total_projects INT;
	SELECT SUM(score), COUNT(*) INTO total_score, total_projects
	FROM corrections WHERE user_id = user_id;

	UPDATE users
	SET users.average_score = IF(total_projects = 0, 0, total_score / total_projects)
	WHERE users.id = user_id;
END //
DELIMITER ;
