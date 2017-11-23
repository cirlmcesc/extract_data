/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50720
 Source Host           : 127.0.0.1
 Source Database       : db_min_test

 Target Server Type    : MySQL
 Target Server Version : 50720
 File Encoding         : utf-8

 Date: 11/23/2017 10:23:57 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `legal_cluster`
-- ----------------------------
DROP TABLE IF EXISTS `legal_cluster`;
CREATE TABLE `legal_cluster` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `province` varchar(100) DEFAULT NULL COMMENT '省市名称',
  `count` int(100) DEFAULT NULL COMMENT '总条数',
  `code` int(100) DEFAULT NULL COMMENT '代码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- ----------------------------
--  Table structure for `legal_data`
-- ----------------------------
DROP TABLE IF EXISTS `legal_data`;
CREATE TABLE `legal_data` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `issued_number` varchar(255) DEFAULT NULL COMMENT '发文字号',
  `timeliness` varchar(255) DEFAULT NULL COMMENT '时效性',
  `release_date` varchar(255) DEFAULT NULL COMMENT '发布日期',
  `implementation_date` varchar(255) DEFAULT NULL COMMENT '实施日期',
  `publishing_department` varchar(255) DEFAULT NULL COMMENT '发布部门',
  `potency_level` varchar(255) DEFAULT NULL COMMENT '效力级别',
  `legal_category` varchar(255) DEFAULT NULL COMMENT '法规类别',
  `cluster_id` int(100) DEFAULT NULL COMMENT '发布部门代码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

SET FOREIGN_KEY_CHECKS = 1;
