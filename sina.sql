CREATE DATABASE IF NOT EXISTS `weibo`;
USE `weibo`;

CREATE TABLE IF NOT EXISTS `posts` (
  `id` bigint(16) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint(16) unsigned NOT NULL,
  `post_id` bigint(16) unsigned NOT NULL,
  `content` mediumtext NOT NULL,
  `add_time` int(10) DEFAULT NULL,
  `attitudes_count` int(10) DEFAULT NULL,
  `comments_count` int(10) DEFAULT NULL,
  `retweet_content` mediumtext,
  `retweet_id` bigint(16) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
