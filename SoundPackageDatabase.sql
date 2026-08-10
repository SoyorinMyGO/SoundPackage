-- 1. voice 表
CREATE TABLE voice (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    alias VARCHAR(50),
    position VARCHAR(100) NOT NULL,
    length INT NOT NULL CHECK (length < 600000),
    used_times INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. package 表
CREATE TABLE package (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    alias VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. tag 表
CREATE TABLE tag (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 4. voice_belong_package 表
CREATE TABLE voice_belong_package (
    id INT PRIMARY KEY AUTO_INCREMENT,
    voice_id INT NOT NULL,
    package_id INT NOT NULL,
    FOREIGN KEY (voice_id) REFERENCES voice(id),
    FOREIGN KEY (package_id) REFERENCES package(id),
    UNIQUE KEY (voice_id, package_id)
);

-- 5. tag_related 表（标签层级关系）
CREATE TABLE tag_related (
    id INT PRIMARY KEY AUTO_INCREMENT,
    parent_id INT NOT NULL,
    child_id INT NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES tag(id),
    FOREIGN KEY (child_id) REFERENCES tag(id),
    UNIQUE KEY (parent_id, child_id)
);

-- 6. voice_belong_tag 表（修正表名和字段名）
CREATE TABLE voice_belong_tag (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tag_id INT NOT NULL,
    voice_id INT NOT NULL,
    FOREIGN KEY (tag_id) REFERENCES tag(id),
    FOREIGN KEY (voice_id) REFERENCES voice(id),
    UNIQUE KEY (tag_id, voice_id)
);