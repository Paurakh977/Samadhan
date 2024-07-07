-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 07, 2024 at 03:55 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `samadhandb`
--

-- --------------------------------------------------------

--
-- Table structure for table `app_usage_info`
--

CREATE TABLE `app_usage_info` (
  `tab_name` varchar(100) NOT NULL,
  `used_time` int(11) NOT NULL,
  `browser` varchar(100) DEFAULT NULL,
  `SN` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app_usage_info`
--

INSERT INTO `app_usage_info` (`tab_name`, `used_time`, `browser`, `SN`) VALUES
('chatgpt', 17, 'Microsoft Edge', 47),
('youtube', 13, 'Microsoft Edge', 48),
('rssnepal', 20, 'Google Chrome', 49);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `app_usage_info`
--
ALTER TABLE `app_usage_info`
  ADD PRIMARY KEY (`SN`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `app_usage_info`
--
ALTER TABLE `app_usage_info`
  MODIFY `SN` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
