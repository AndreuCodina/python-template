CREATE TABLE products(
    id UUID NOT NULL,
    name TEXT NOT NULL,
    description TEXT NULL,
    price DECIMAL NOT NULL,
    is_discontinued BOOLEAN NOT NULL,
    discontinuation_reason TEXT NULL,
    CONSTRAINT products_pkey PRIMARY KEY(id)
);