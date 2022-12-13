CREATE TABLE IF NOT EXISTS Person (
	user_id SERIAL,
	username VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS Post (
	post_id SERIAL,
	title VARCHAR(255) NOT NULL,
	creature VARCHAR(255) NOT NULL,
	user_id INT NOT NULL,
    place VARCHAR(255) NOT NULL,
	description TEXT, 
	photo_path VARCHAR(255) NOT NULL,
    likes INT NOT NULL,
	dislikes INT NOT NULL,
	PRIMARY KEY (post_id),
	FOREIGN KEY (user_id) REFERENCES Person(user_id)
);


CREATE TABLE IF NOT EXISTS Comment (
	comment_id SERIAL,
	post_id SERIAL,
	text TEXT NOT NULL,
	user_id SERIAL,
    time_stamp TIMESTAMP NOT NULL,
	likes INT NOT NULL,
	dislikes INT NOT NULL,
	PRIMARY KEY(comment_id),
	FOREIGN KEY (post_id) REFERENCES Post(post_id),
	FOREIGN KEY (user_id) REFERENCES Person(user_id)
);

CREATE TABLE IF NOT EXISTS CommentLikes (
	comment_id SERIAL,
	user_id SERIAL,
	PRIMARY KEY(comment_id),
	FOREIGN KEY (comment_id) REFERENCES Comment(comment_id),
	FOREIGN KEY (user_id) REFERENCES Person(user_id)
);

CREATE TABLE IF NOT EXISTS CommentDislikes (
	comment_id SERIAL,
	user_id SERIAL,
	PRIMARY KEY(comment_id),
	FOREIGN KEY (comment_id) REFERENCES Comment(comment_id),
	FOREIGN KEY (user_id) REFERENCES Person(user_id)
);

CREATE TABLE IF NOT EXISTS PostLikes (
	post_id SERIAL,
	user_id SERIAL,
	PRIMARY KEY(post_id),
	FOREIGN KEY (post_id) REFERENCES Post(post_id),
	FOREIGN KEY (user_id) REFERENCES Person(user_id)
);

CREATE TABLE IF NOT EXISTS PostDislikes (
	post_id SERIAL,
	user_id SERIAL,
	PRIMARY KEY(post_id),
	FOREIGN KEY (post_id) REFERENCES Post(psot_id),
	FOREIGN KEY (user_id) REFERENCES Person(user_id)
);
