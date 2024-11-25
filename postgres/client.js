const { Client } = require('pg');

const pgclient = new Client({
    host: process.env.POSTGRES_HOST,
    port: process.env.POSTGRES_PORT,
    user: 'postgres',
    password: 'postgres',
    database: 'postgres'
});

pgclient.connect();

pgclient.query('SELECT NOW()', (err, res) => {
    if (err) throw err
    console.log(res)
    pgclient.end()
});

const createTableQuery = `
    CREATE TABLE IF NOT EXISTS binbot_user (
        id UUID PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        is_active BOOLEAN NOT NULL,
        role VARCHAR(50) NOT NULL,
        full_name VARCHAR(255),
        password VARCHAR(40) NOT NULL,
        username VARCHAR(50) UNIQUE
    )
`;

pgclient.query(createTableQuery, (err, res) => {
    if (err) throw err;
    console.log('Table created or already exists');

    const insertUserQuery = `
        INSERT INTO binbot_user (id, email, is_active, role, full_name, password, username)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
    `;

    const user = {
        id: 'some-uuid',
        email: 'user@example.com',
        isActive: true,
        role: 'admin',
        fullName: 'John Doe',
        password: 'securepassword',
        username: 'johndoe'
    };

    pgclient.query(insertUserQuery, [
        user.id, user.email, user.isActive, user.role, user.fullName, user.password, user.username
    ], (err, res) => {
        if (err) throw err;
        console.log('User inserted successfully');
        pgclient.end();
    });
});
