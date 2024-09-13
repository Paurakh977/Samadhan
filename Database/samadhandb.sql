-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 10, 2024 at 03:29 PM
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
  `used_date` date DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `serial_id` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app_usage_info`
--

INSERT INTO `app_usage_info` (`tab_name`, `used_time`, `browser`, `SN`, `used_day`, `used_date`, `email`, `serial_id`) VALUES
(' Visual Studio Code', 42, NULL, 54, 'Thursday', '2024-08-29', 'dollarchaeyo@gmail.com', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('replit', 18, NULL, 55, 'Thursday', '2024-08-29', 'dollarchaeyo@gmail.com', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('whatsapp', 6, NULL, 56, 'Thursday', '2024-08-29', 'dollarchaeyo@gmail.com', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('youtube', 3, NULL, 57, 'Thursday', '2024-08-29', 'dollarchaeyo@gmail.com', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('php?route=/sql&pos=0&db=samadhandb&table=app_usage_info', 3, NULL, 61, 'Thursday', '2024-08-29', 'dollarchaeyo@gmail.com', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('Task Switching', 3, NULL, 63, 'Thursday', '2024-08-29', 'paurakh.pandey@sifal.deerwalk.edu.np', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('SAMADHAN', 9, NULL, 64, 'Thursday', '2024-08-29', 'paurakh.pandey@sifal.deerwalk.edu.np', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('youtube', 54, NULL, 65, 'Thursday', '2024-08-29', 'paurakh.pandey@sifal.deerwalk.edu.np', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('replit', 3, NULL, 66, 'Thursday', '2024-08-29', 'paurakh.pandey@sifal.deerwalk.edu.np', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('google', 78, NULL, 67, 'Thursday', '2024-08-29', 'paurakh.pandey@sifal.deerwalk.edu.np', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
(' Visual Studio Code', 15, NULL, 68, 'Saturday', '2024-08-31', 'paurakh.pandey@sifal.deerwalk.edu.np', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('google', 54, NULL, 69, 'Saturday', '2024-08-31', 'paurakh.pandey@sifal.deerwalk.edu.np', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('Task Switching', 3, NULL, 70, 'Saturday', '2024-08-31', 'paurakh.pandey@sifal.deerwalk.edu.np', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('php?route=/sql&pos=0&db=samadhandb&table=app_usage_info', 63, NULL, 71, 'Saturday', '2024-08-31', 'paurakh.pandey@sifal.deerwalk.edu.np', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('facebook', 6, NULL, 72, 'Saturday', '2024-08-31', 'paurakh.pandey@sifal.deerwalk.edu.np', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('Clock', 15, NULL, 73, 'Saturday', '2024-08-31', 'paurakh.pandey@sifal.deerwalk.edu.np', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
(' Visual Studio Code', 27, NULL, 74, 'Saturday', '2024-08-31', 'dada@gmail.com', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('Search', 6, NULL, 75, 'Saturday', '2024-08-31', 'dada@gmail.com', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('Clock', 126, NULL, 76, 'Saturday', '2024-08-31', 'dada@gmail.com', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('php?route=/sql&pos=0&db=samadhandb&table=user_info_google', 3, NULL, 77, 'Saturday', '2024-08-31', 'dada@gmail.com', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
('php?route=/sql&pos=0&db=samadhandb&table=app_usage_info', 18, NULL, 78, 'Saturday', '2024-08-31', 'dada@gmail.com', 'f8a294e2-f241-4eca-a964-c0c88c21f3c2');

-- --------------------------------------------------------

--
-- Table structure for table `info`
--

CREATE TABLE `info` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(2) NOT NULL,
  `time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(5, 'paurakh.pandey@sifal.deerwalk.edu.np', 'Paurakh Raj Pandey', NULL, 0, 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
(6, 'dollarchaeyo@gmail.com', 'Dollar Chaeyo', NULL, 0, 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
(7, 'pandeypaurakhraj@gmail.com', 'Paurakh Raj Pandey', NULL, 0, 'f8a294e2-f241-4eca-a964-c0c88c21f3c2'),
(8, 'yareyaredazey108@gmail.com', 'Jet Blackwing', NULL, 1, '1bcfadd1-06b5-4086-b4e9-a5ae90da5af5'),
(10, 'yareyaredazey108@gmail.com', 'Jet Blackwing', NULL, 1, '1bcfadd1-06b5-4086-b4e9-a5ae90da5af5');

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
-- Indexes for table `info`
--
ALTER TABLE `info`
  ADD PRIMARY KEY (`id`);

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
  MODIFY `SN` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- AUTO_INCREMENT for table `info`
--
ALTER TABLE `info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_info_google`
--
ALTER TABLE `user_info_google`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `user_info_manual`
--
ALTER TABLE `user_info_manual`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
