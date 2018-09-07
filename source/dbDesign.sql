-- 创建豆瓣数据库
CREATE DATABASE `douban` CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
-- 创建电影基本列表 多个标签用 \t 分隔开
CREATE TABLE `film_list` (
  `subject` int(12) PRIMARY KEY NOT NULL COMMENT '链接ID',
  `title` varchar(100) DEFAULT NULL COMMENT '电影名称',
  `alias` varchar(100) DEFAULT NULL COMMENT '又名',
  `director` varchar(300) DEFAULT NULL COMMENT '导演',
  `writer` varchar(500) DEFAULT NULL COMMENT '编剧',
  `starring` varchar(3000) DEFAULT NULL COMMENT '主演',
  `classification` varchar(150) DEFAULT NULL COMMENT '类型',
  `country` varchar(150) DEFAULT NULL COMMENT '制片国家/地区',
  `language` varchar(150) DEFAULT NULL COMMENT '语言',
  `score` float(2,1) DEFAULT NULL COMMENT '评分',
  `ratio` varchar(100) DEFAULT NULL COMMENT '分类排位百分比',
  `release_date` varchar(100) DEFAULT NULL COMMENT '上映日期',
  `film_length` varchar(1000) DEFAULT NULL COMMENT '片长',
  `introduction` varchar(10000) DEFAULT NULL COMMENT '剧情简介',
  `common_label` varchar(200) DEFAULT NULL COMMENT '常用标签',
  `seen_quantity` int(12) DEFAULT NULL COMMENT '看过的人数',
  `want_to_see` int(12) DEFAULT NULL COMMENT '想看的人数',
  `num1` int(5) DEFAULT NULL COMMENT '保留字段1',
  `num2` int(10) DEFAULT NULL COMMENT '参与评分人数',
  `num3` int(15) DEFAULT NULL COMMENT '保留字段3',
  `stra` varchar(50) DEFAULT NULL COMMENT '保留字段a',
  `strb` varchar(100) DEFAULT NULL COMMENT '封面图片链接',
  `strc` varchar(150) DEFAULT NULL COMMENT '保留字段c',
  `strd` varchar(200) DEFAULT NULL COMMENT '保留字段d',
  `stre` varchar(250) DEFAULT NULL COMMENT '保留字段e'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `user_list` (
  `uname` varchar(16) PRIMARY KEY NOT NULL COMMENT '用户名',
  `email` varchar(20) NOT NULL COMMENT '邮箱',
  `passwd` varchar(18) NOT NULL COMMENT '密码',
  `viewed` varchar(1000) DEFAULT NULL COMMENT '观影记录'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
