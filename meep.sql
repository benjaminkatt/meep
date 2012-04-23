SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `meep` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ;
USE `meep` ;

-- -----------------------------------------------------
-- Table `meep`.`USER`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `meep`.`USER` (
  `Username` VARCHAR(45) NOT NULL ,
  `Password` VARCHAR(45) NOT NULL ,
  `ID` INT NOT NULL ,
  PRIMARY KEY (`ID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `meep`.`MESSAGE`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `meep`.`MESSAGE` (
  `ID` INT NOT NULL ,
  `Title` VARCHAR(45) NOT NULL ,
  `Post` VARCHAR(2000) NOT NULL ,
  `parentID` INT NOT NULL ,
  `USER_ID` INT NOT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_MESSAGE_USER` (`USER_ID` ASC) ,
  CONSTRAINT `fk_MESSAGE_USER`
    FOREIGN KEY (`USER_ID` )
    REFERENCES `meep`.`USER` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `meep`.`SESSION`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `meep`.`SESSION` (
  `ID` VARCHAR(128) NOT NULL ,
  `USER_ID` INT NOT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_SESSION_USER1` (`USER_ID` ASC) ,
  CONSTRAINT `fk_SESSION_USER1`
    FOREIGN KEY (`USER_ID` )
    REFERENCES `meep`.`USER` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
