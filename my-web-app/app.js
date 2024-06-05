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

app.get('/', async (req, res) => {
    try {
        const query = `
            SELECT p."Name", p."Img", p."Link", 
                   s."Size", s."Shoulder Width", s."Chest Circumference", 
                   s."Hem Width", s."Sleeve Length", s."Sleeve Opening", s."Total Length"
            FROM byslim_products p
            LEFT JOIN byslim_size_info s ON p."Name" = s."Name"
        `;

        const result = await pool.query(query);
        const products = result.rows;

        console.log(products); // 디버깅을 위해 데이터 출력

        res.render('index', { products });
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500).send('Server Error');
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
