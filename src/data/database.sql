
CREATE TABLE [type] (
[id] VARCHAR(64) PRIMARY KEY NOT NULL,
[name] VARCHAR(255) NOT NULL);

INSERT INTO type VALUES ("", "Folder");
INSERT INTO type VALUES ("image", "Image");
INSERT INTO type VALUES ("video", "Video");
INSERT INTO type VALUES ("audio", "Audio");
INSERT INTO type VALUES ("text", "Text");
INSERT INTO type VALUES ("bin", "Binary");



CREATE TABLE [extension] (
[id] VARCHAR(32) PRIMARY KEY NOT NULL,
[type] VARCHAR(64) NULL,
[name] VARCHAR(32) NULL);




CREATE TABLE [host] (
[id] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
[path] TEXT NOT NULL,
[name] TEXT UNIQUE NOT NULL);



CREATE TABLE [root] (
[id] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
[root] TEXT NOT NULL,
[host] INTEGER NULL,
[updated] TEXT NULL);



CREATE TABLE [file] (
[id] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
[root] TEXT NULL,
[url] TEXT NOT NULL,
[extension] TEXT NULL,
[name] TEXT NOT NULL,
[size] INTEGER NULL,
[hash] TEXT NULL,
[created] TEXT NULL,
[modified] TEXT NULL);
