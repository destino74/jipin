CREATE DATABASE  IF NOT EXISTS recruitment CHARACTER SET utf8;

CREATE TABLE IF NOT EXISTS recruitment_source (
  id INT NOT NULL AUTO_INCREMENT COMMENT '平台id',
  name VARCHAR(255) NOT NULL DEFAULT '' COMMENT '平台名',
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS recruitment_detail (
  id INT(10) NOT NULL AUTO_INCREMENT ,
  title VARCHAR(255) NOT NULL DEFAULT '' COMMENT '职位名称',
  salary VARCHAR(255) NOT NULL DEFAULT '' COMMENT '薪水',
  province VARCHAR(255) NOT NULL DEFAULT '' COMMENT '省份',
  experience VARCHAR(255) NOT NULL DEFAULT '' COMMENT '经验',
  education VARCHAR(255) NOT NULL DEFAULT '' COMMENT '学历',
  content VARCHAR(255) NOT NULL DEFAULT '' COMMENT '职位描述',
  address VARCHAR(255) NOT NULL DEFAULT '' COMMENT '地址',
  url VARCHAR(255) NOT NULL DEFAULT '' COMMENT '源URL',
  company VARCHAR(255) NOT NULL DEFAULT '' COMMENT '公司名',
  icon VARCHAR(255) NOT NULL DEFAULT '' COMMENT '公司ICON',
  source_id INT NOT NULL COMMENT '平台id',
  detail_id INT NOT NULL COMMENT '平台职位id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `source_detail` (`source_id`, `detail_id`)
)

