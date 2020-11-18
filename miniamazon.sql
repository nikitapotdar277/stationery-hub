-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 18, 2020 at 12:49 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `miniamazon`
--

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `item_id` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `item_name` varchar(50) NOT NULL,
  `price` float NOT NULL,
  `item_type` varchar(10) NOT NULL,
  `img` blob NOT NULL,
  `sold` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`item_id`, `email`, `item_name`, `price`, `item_type`, `img`, `sold`) VALUES
(10, 'nikita.potdar15@gmail.com', 'mini-drafter', 330, 'sell', '', 0),
(11, 'nikita.potdar15@gmail.com', 'drafter', 0, 'lend', '', 1),
(12, 'nikita.potdar008@gmail.com', 'drafter', 350, 'sell', '', 0);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `item_name` varchar(50) NOT NULL,
  `price` float NOT NULL,
  `seller` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `email`, `item_name`, `price`, `seller`) VALUES
(1, 'nikita.potdar008@gmail.com', 'drafter', 0, 'nikita.potdar15@gmail.com'),
(2, 'nikita.potdar008@gmail.com', 'drafter', 0, 'nikita.potdar15@gmail.com'),
(3, 'nikita.potdar008@gmail.com', 'drafter', 0, 'nikita.potdar15@gmail.com'),
(4, 'nikita.potdar008@gmail.com', 'drafter', 0, 'nikita.potdar15@gmail.com'),
(5, 'nikita.potdar008@gmail.com', 'drafter', 0, 'nikita.potdar15@gmail.com'),
(6, 'nikita.potdar008@gmail.com', 'drafter', 0, 'nikita.potdar15@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE `registration` (
  `email` varchar(50) DEFAULT NULL,
  `branch` varchar(36) DEFAULT NULL,
  `year` varchar(3) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`email`, `branch`, `year`, `password`, `user_id`) VALUES
('yelaiyugandhar@gmail.com', 'Computer', 'TE', 'pass', 1),
('sakship1920@gmail.com', 'Computer', 'TE', 'ppp', 3),
('nikita.potdar15@gmail.com', 'Computer', 'TE', '1234', 4),
('123@123.com', 'Mechanical', 'TE', '1111', 5),
('nikita.potdar008@gmail.com', 'Computer', 'TE', '0000', 6);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`item_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`);

--
-- Indexes for table `registration`
--
ALTER TABLE `registration`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `items`
--
ALTER TABLE `items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `registration`
--
ALTER TABLE `registration`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
