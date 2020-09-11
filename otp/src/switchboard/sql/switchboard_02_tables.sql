USE switchboard;

DROP TABLE IF EXISTS playerinfo;
drop table if exists recipientmail;


CREATE TABLE playerinfo (
  playerId             BIGINT      NOT NULL,
  avatarName           VARCHAR(64) NOT NULL,
  playerName           VARCHAR(64) NOT NULL,
  openChatEnabledYesNo TINYINT     NOT NULL,
  location             VARCHAR(64) NOT NULL,
  sublocation          VARCHAR(64) NOT NULL,
  lastupdate           TIMESTAMP   NOT NULL 
                         DEFAULT   CURRENT_TIMESTAMP 
                         ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (playerId) 
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8;


CREATE TABLE recipientmail (
  messageId             BIGINT     NOT NULL AUTO_INCREMENT,
  recipientId           BIGINT     NOT NULL,
  senderId              BIGINT     NOT NULL,
  message               TEXT       NOT NULL,
  lastupdate            TIMESTAMP  NOT NULL 
                         DEFAULT   CURRENT_TIMESTAMP
                         ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY  (messageId),
  INDEX idx_recipientId (recipientId)
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8;