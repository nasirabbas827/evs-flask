-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 09, 2024 at 11:46 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `evs_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `candidates`
--

CREATE TABLE `candidates` (
  `candidate_id` int(11) NOT NULL,
  `candidate_picture` varchar(255) DEFAULT NULL,
  `candidate_name` varchar(255) NOT NULL,
  `candidate_party` varchar(255) DEFAULT NULL,
  `motive` text DEFAULT NULL,
  `election_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `candidates`
--

INSERT INTO `candidates` (`candidate_id`, `candidate_picture`, `candidate_name`, `candidate_party`, `motive`, `election_id`) VALUES
(1, 'Age_and_gender_2.jpg', 'Abbas', 'PMLN', 'dasg', 1),
(2, 'Age_and_Gender.jpg', 'Abbas', 'PMLN', 'dsagd', 1),
(3, 'WhatsApp_Image_2024-01-26_at_9.25.10_PM.jpeg', 'Nasir', 'PMLN', 'adsfa', 1),
(4, 'WhatsApp_Image_2024-01-25_at_1.43.58_PM.jpeg', 'Nasir', 'PMLN', 'saffd', 10),
(5, 'WhatsApp_Image_2024-01-25_at_12.01.34_PM.jpeg', 'Haider', 'PMLN', 'dfs', 8);

-- --------------------------------------------------------

--
-- Table structure for table `elections`
--

CREATE TABLE `elections` (
  `election_id` int(11) NOT NULL,
  `election_name` varchar(255) NOT NULL,
  `status` enum('pending','ongoing','completed') NOT NULL DEFAULT 'pending',
  `start_date` date NOT NULL,
  `end_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `elections`
--

INSERT INTO `elections` (`election_id`, `election_name`, `status`, `start_date`, `end_date`) VALUES
(1, 'First election', 'completed', '2024-02-09', '2024-02-09'),
(2, 'Election 1', 'pending', '2024-02-10', '2024-02-20'),
(3, 'Election 2', 'pending', '2024-02-15', '2024-02-25'),
(4, 'Election 3', 'ongoing', '2024-02-20', '2024-03-01'),
(5, 'Election 4', 'ongoing', '2024-02-25', '2024-03-05'),
(6, 'Election 5', 'completed', '2024-03-01', '2024-03-10'),
(7, 'Election 6', 'completed', '2024-03-05', '2024-03-15'),
(8, 'Election 7', 'pending', '2024-03-10', '2024-03-20'),
(9, 'Election 8', 'ongoing', '2024-03-15', '2024-03-25'),
(10, 'Election 9', 'completed', '2024-03-20', '2024-03-30'),
(11, 'Election 10', 'ongoing', '2024-03-25', '2024-04-04');

-- --------------------------------------------------------

--
-- Table structure for table `voters`
--

CREATE TABLE `voters` (
  `voter_id` int(11) NOT NULL,
  `voter_name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `voters`
--

INSERT INTO `voters` (`voter_id`, `voter_name`, `username`, `password`) VALUES
(1, 'Nasir', 'nasir123', 'pbkdf2:sha256:600000$rNKJr4HVbbeJsdXT$26d099e77e54121d4cffa813f5cb64e89a075da0aa7779c804e45614298e8288'),
(2, 'Nasir abbas', 'haider12', 'pbkdf2:sha256:600000$PvQo768LqR5DndZs$c368bb24ca5d180b7b87191350422c00b412d0c538f0f7794821d1b20973b4c3'),
(3, 'Haider', 'Haider123', 'pbkdf2:sha256:600000$MnoBTrfTHYuUkxeM$8c55aaa52788f4725787b5ebfd3797908298ac4355ce2f445af8123579e2553f');

-- --------------------------------------------------------

--
-- Table structure for table `votes`
--

CREATE TABLE `votes` (
  `vote_id` int(11) NOT NULL,
  `voter_id` int(11) DEFAULT NULL,
  `candidate_id` int(11) DEFAULT NULL,
  `election_id` int(11) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `block_id` int(11) DEFAULT NULL,
  `block_hash` varchar(255) DEFAULT NULL,
  `previous_block_hash` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `votes`
--

INSERT INTO `votes` (`vote_id`, `voter_id`, `candidate_id`, `election_id`, `timestamp`, `block_id`, `block_hash`, `previous_block_hash`) VALUES
(13, 1, 3, 1, '2024-02-09 10:09:54', 1, '11e14da10a1b2a8d75c1aece065fda94a489b25680e67560783ec5544cd1ac5c', '264ee1fc6b2466602c381acac7e2d8630732acde55bb38e9f769983669b5b94e'),
(14, 1, 4, 10, '2024-02-09 10:11:03', 2, '272c1aec874168e91f31b570aaee5a1cbd1ac7654d1fc317c614c14d4f3306b3', '11e14da10a1b2a8d75c1aece065fda94a489b25680e67560783ec5544cd1ac5c'),
(15, 3, 3, 1, '2024-02-09 10:11:54', 3, 'da344a1a27be3a28e934536e325482de590562e0d3b2b5071ba4b1dd4bda5316', '272c1aec874168e91f31b570aaee5a1cbd1ac7654d1fc317c614c14d4f3306b3');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `candidates`
--
ALTER TABLE `candidates`
  ADD PRIMARY KEY (`candidate_id`),
  ADD KEY `election_id` (`election_id`);

--
-- Indexes for table `elections`
--
ALTER TABLE `elections`
  ADD PRIMARY KEY (`election_id`);

--
-- Indexes for table `voters`
--
ALTER TABLE `voters`
  ADD PRIMARY KEY (`voter_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `votes`
--
ALTER TABLE `votes`
  ADD PRIMARY KEY (`vote_id`),
  ADD KEY `voter_id` (`voter_id`),
  ADD KEY `candidate_id` (`candidate_id`),
  ADD KEY `election_id` (`election_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `candidates`
--
ALTER TABLE `candidates`
  MODIFY `candidate_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `elections`
--
ALTER TABLE `elections`
  MODIFY `election_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `voters`
--
ALTER TABLE `voters`
  MODIFY `voter_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `votes`
--
ALTER TABLE `votes`
  MODIFY `vote_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `candidates`
--
ALTER TABLE `candidates`
  ADD CONSTRAINT `candidates_ibfk_1` FOREIGN KEY (`election_id`) REFERENCES `elections` (`election_id`);

--
-- Constraints for table `votes`
--
ALTER TABLE `votes`
  ADD CONSTRAINT `votes_ibfk_1` FOREIGN KEY (`voter_id`) REFERENCES `voters` (`voter_id`),
  ADD CONSTRAINT `votes_ibfk_2` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`candidate_id`),
  ADD CONSTRAINT `votes_ibfk_3` FOREIGN KEY (`election_id`) REFERENCES `elections` (`election_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
