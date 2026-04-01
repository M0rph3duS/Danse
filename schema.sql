DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS salle;
DROP TABLE IF EXISTS prof;
DROP TABLE IF EXISTS niveau;
DROP TABLE IF EXISTS info_ecole;
DROP TABLE IF EXISTS danse;
DROP TABLE IF EXISTS info_ecole;



CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,

    date_naissance TEXT NOT NULL, -- format AAAA-MM-JJ (validé côté Python)

    telephone1 TEXT,
    telephone2 TEXT,
    email TEXT,

    adresse TEXT,
    ville TEXT,
    code_postal INTEGER,

    role TEXT CHECK(role IN ('Leader','Follower')) NOT NULL,
    profession TEXT,
    rencontre TEXT CHECK(rencontre IN (
        'Bouche à oreille',
        'Portes ouvertes',
        'Affiches magasins',
        'Site internet',
        'Réseaux sociaux',
        'Flyers',
        'Autres'
    )) NOT NULL,

    annee_inscription INTEGER CHECK(annee_inscription >= 1900),

    commentaire TEXT DEFAULT '',
    commentaire_paiement TEXT DEFAULT '',

    montant_du DECIMAL DEFAULT 0,
    montant_regle DECIMAL DEFAULT 0,

    champ_extra_1 TEXT DEFAULT '',
    champ_extra_2 TEXT DEFAULT '',

    partner_id INTEGER DEFAULT NULL,
    FOREIGN KEY (partner_id) REFERENCES users(id) ON DELETE SET NULL,
    CHECK(partner_id IS NULL OR partner_id != id)

    UNIQUE(nom, prenom, email)
);

-- -------------------------
-- Table Salle
-- -------------------------
CREATE TABLE salle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE,
    description TEXT DEFAULT '' 
);

-- -------------------------
-- Table Danse
-- -------------------------
CREATE TABLE danse (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE,
    couleur VARCHAR(7) DEFAULT '#FFFFFF',  -- code hex de la couleur (#RRGGBB)
    description TEXT DEFAULT ''
);
-- -------------------------
-- Table Prof
-- -------------------------
CREATE TABLE prof (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    description TEXT DEFAULT ''
);

-- -------------------------
-- Table Niveau
-- -------------------------
CREATE TABLE niveau (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE,
    description TEXT DEFAULT ''
);

-- -------------------------
-- Table Info École
-- -------------------------
CREATE TABLE info_ecole (
    nom TEXT NOT NULL,
    adresse TEXT,
    ville TEXT,
    telephone TEXT,
    code_postal TEXT,
    heure_debut_planning TEXT,
    heure_fin_planning TEXT,
    jour_debut_planning TEXT,
    jour_fin_planning TEXT
    
);

CREATE TABLE cours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    danse_id INTEGER NOT NULL,
    niveau_id INTEGER NOT NULL,
    salle_id INTEGER NOT NULL,
    saison TEXT NOT NULL,

    jour TEXT NOT NULL,
    heure_debut TEXT NOT NULL,
    heure_fin TEXT NOT NULL,
    commentaires TEXT DEFAULT '',

    FOREIGN KEY (danse_id) REFERENCES danse(id),
    FOREIGN KEY (niveau_id) REFERENCES niveau(id),
    FOREIGN KEY (salle_id) REFERENCES salle(id)
);

CREATE TABLE cours_prof (
    cours_id INTEGER,
    prof_id INTEGER,
    saison TEXT NOT NULL,

    PRIMARY KEY (cours_id, prof_id),

    FOREIGN KEY (cours_id) REFERENCES cours(id) ON DELETE CASCADE,
    FOREIGN KEY (prof_id) REFERENCES prof(id)
);

CREATE INDEX idx_cours_saison ON cours(saison);
CREATE INDEX idx_cours_prof_saison ON cours_prof(saison);