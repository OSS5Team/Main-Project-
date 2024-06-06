const express = require('express');
const { Pool } = require('pg');
const app = express();
const port = 3000;

const pool = new Pool({
    host: 'localhost',
    database: 'test',
    user: 'Test',
    password: '1234',
    port: 5432, // PostgreSQL 기본 포트
});

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

app.get('/', async (req, res) => {
    try {
        const { name, size, shoulder_width, chest_circumference, hem_width, sleeve_length, sleeve_opening, total_length } = req.query;

        let query = `
            SELECT p."Name", p."Img", p."Link", 
                   s."Size", s."Shoulder Width", s."Chest Circumference", 
                   s."Hem Width", s."Sleeve Length", s."Sleeve Opening", s."Total Length"
            FROM byslim_products p
            LEFT JOIN byslim_size_info s ON p."Name" = s."Name"
            UNION
            SELECT p."Name", p."Img", p."Link", 
                   s."Size", s."Shoulder Width", s."Chest Circumference", 
                   s."Hem Width", s."Sleeve Length", s."Sleeve Opening", s."Total Length"
            FROM lookple_products p
            LEFT JOIN lookple_size_info s ON p."Name" = s."Name"
            WHERE 1=1
        `;

        const queryParams = [];
        if (name) {
            query += ` AND p."Name" ILIKE $${queryParams.length + 1}`;
            queryParams.push(`%${name}%`);
        }
        if (size) {
            query += ` AND s."Size" = $${queryParams.length + 1}`;
            queryParams.push(size);
        }
        if (shoulder_width) {
            query += ` AND s."Shoulder Width"::int >= $${queryParams.length + 1}`;
            queryParams.push(shoulder_width);
        }
        if (chest_circumference) {
            query += ` AND s."Chest Circumference"::int >= $${queryParams.length + 1}`;
            queryParams.push(chest_circumference);
        }
        if (hem_width) {
            query += ` AND s."Hem Width"::int >= $${queryParams.length + 1}`;
            queryParams.push(hem_width);
        }
        if (sleeve_length) {
            query += ` AND s."Sleeve Length"::int >= $${queryParams.length + 1}`;
            queryParams.push(sleeve_length);
        }
        if (sleeve_opening) {
            query += ` AND s."Sleeve Opening"::int >= $${queryParams.length + 1}`;
            queryParams.push(sleeve_opening);
        }
        if (total_length) {
            query += ` AND s."Total Length"::int >= $${queryParams.length + 1}`;
            queryParams.push(total_length);
        }

        const result = await pool.query(query, queryParams);
        const products = result.rows;

        res.render('index', { products });
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500).send('Server Error');
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
