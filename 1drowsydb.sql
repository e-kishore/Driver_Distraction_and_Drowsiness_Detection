-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 11, 2022 at 07:34 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `1drowsydb`
--

-- --------------------------------------------------------

--
-- Table structure for table `ownertb`
--

CREATE TABLE `ownertb` (
  `id` bigint(250) NOT NULL auto_increment,
  `OwnerName` varchar(250) NOT NULL,
  `CompanyName` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `ownertb`
--

INSERT INTO `ownertb` (`id`, `OwnerName`, `CompanyName`, `Mobile`, `Email`, `Address`) VALUES
(1, 'san', 'Abcd', '9486365535', 'sangeeth5535@gmail.com', 'no 6 trichy'),
(2, 'san', 'Rajiya', '9486365535', 'sangeeth5535@gmail.com', 'no 6 trichy'),
(3, 'Harini', 'HariniTra', '8072656704', 'harinisachidanandham01@gmail.com', 'no');

-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `id` bigint(20) NOT NULL auto_increment,
  `CompanyName` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `EmailId` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `Licence` varchar(250) NOT NULL,
  `Aadhar` varchar(250) NOT NULL,
  `Experience` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`id`, `CompanyName`, `Mobile`, `EmailId`, `Address`, `Licence`, `Aadhar`, `Experience`, `UserName`, `Password`) VALUES
(1, 'Abcd', '9486365535', 'sangeeth5535@gmail.com', 'no 6 trichy', '2365347654', '4376347', '4', 'sangeeth', 'sangeeth'),
(2, 'Rajiya', '9486365535', 'sangeeth5535@gmail.com', 'no 6 trichy', '2365347654', '4376347', '4', 'raji', 'raji'),
(3, 'HariniTra', '8072656704', 'harinisachidanandham01@gmail.com', 'no', '2353265436464', '2352346457', '4', 'harini', 'harini');
