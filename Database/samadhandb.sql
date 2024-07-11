-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 11, 2024 at 09:00 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

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
  `SN` int(11) NOT NULL,
  `used_day` varchar(10) DEFAULT NULL,
  `used_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app_usage_info`
--

INSERT INTO `app_usage_info` (`tab_name`, `used_time`, `browser`, `SN`, `used_day`, `used_date`) VALUES
('localhost/phpmyadmin/index', 5, 'Google Chrome', 1, 'Tuesday', '2024-07-09'),
('youtube', 15, 'Firefox', 2, 'Wednesday', '2024-07-10'),
('instagram', 20, 'Safari', 3, 'Thursday', '2024-07-11'),
('facebook', 45, 'Opera', 4, 'Friday', '2024-07-12'),
('twitter', 30, 'Microsoft Edge', 5, 'Saturday', '2024-07-13'),
('reddit', 10, 'Google Chrome', 6, 'Sunday', '2024-07-14'),
('whatsapp', 35, 'Safari', 8, 'Tuesday', '2024-07-16'),
('snapchat', 40, 'Opera', 9, 'Wednesday', '2024-07-17'),
('tiktok', 50, 'Microsoft Edge', 10, 'Thursday', '2024-07-18'),
('discord', 7, 'Microsoft Edge', 32, 'Monday', '2024-07-08');

-- --------------------------------------------------------

--
-- Table structure for table `user_info_google`
--

CREATE TABLE `user_info_google` (
  `ID` int(11) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `logged_in_status` tinyint(1) NOT NULL DEFAULT 0,
  `serial_id` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_info_google`
--

INSERT INTO `user_info_google` (`ID`, `email`, `username`, `password`, `logged_in_status`, `serial_id`) VALUES
(2, 'yareyaredazey108@gmail.com', 'Jet Blackwing', NULL, 0, NULL),
(5, 'paurakh.pandey@sifal.deerwalk.edu.np', 'Paurakh Raj Pandey', NULL, 0, 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
(6, 'dollarchaeyo@gmail.com', 'Dollar Chaeyo', NULL, 0, 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
(7, 'pandeypaurakhraj@gmail.com', 'Paurakh Raj Pandey', NULL, 0, 'f8a294e2-f241-4eca-a964-c0c88c21f3c2');

-- --------------------------------------------------------

--
-- Table structure for table `user_info_manual`
--

CREATE TABLE `user_info_manual` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `phnumber` varchar(20) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `radio_button` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `logged_in_status` tinyint(1) DEFAULT 0,
  `serial_id` varchar(256) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_info_manual`
--

INSERT INTO `user_info_manual` (`user_id`, `username`, `phnumber`, `email`, `password`, `radio_button`, `created_at`, `logged_in_status`, `serial_id`) VALUES
(16, 'admin dada', '9876543456', 'admin@gmail.com', '$2b$12$WMDnjnQGHfHlO7xVxtsUj.tNirNjwUqIH65NpQlQfG8Gdb1yX1V7y', 'For myself', '2024-07-11 18:21:21', 0, 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
(17, 'dada', '9810172202', 'dada@gmail.com', '$2b$12$WMDnjnQGHfHlO7xVxtsUj.D6/9.tVkuiVzpezowiOkElQVOcHlXm.', 'For myself', '2024-07-11 18:46:46', 1, 'f8a294e2-f241-4eca-a964-c0c88c21f3c2');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `app_usage_info`
--
ALTER TABLE `app_usage_info`
  ADD PRIMARY KEY (`SN`);

--
-- Indexes for table `user_info_google`
--
ALTER TABLE `user_info_google`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `user_info_manual`
--
ALTER TABLE `user_info_manual`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `app_usage_info`
--
ALTER TABLE `app_usage_info`
  MODIFY `SN` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `user_info_google`
--
ALTER TABLE `user_info_google`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user_info_manual`
--
ALTER TABLE `user_info_manual`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
