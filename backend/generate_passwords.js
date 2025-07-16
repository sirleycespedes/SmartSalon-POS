const bcrypt = require('bcryptjs');

async function generatePasswords() {
  const passwords = ['admin123', 'gerente123', 'empleado123', 'recepcion123'];
  
  console.log('-- Contraseñas hasheadas para usuarios:');
  
  for (let i = 0; i < passwords.length; i++) {
    const hash = await bcrypt.hash(passwords[i], 10);
    console.log(`-- ${passwords[i]} -> ${hash}`);
  }
  
  // Generar SQL con las contraseñas correctas
  const adminHash = await bcrypt.hash('admin123', 10);
  const gerenteHash = await bcrypt.hash('gerente123', 10);
  const empleadoHash = await bcrypt.hash('empleado123', 10);
  const recepcionHash = await bcrypt.hash('recepcion123', 10);
  
  console.log('\n-- SQL para insertar usuarios:');
  console.log(`INSERT INTO usuarios_nestjs (persona_id, tienda_id, role_id, username, email, password_hash) VALUES`);
  console.log(`(1, 1, 1, 'admin', 'admin@barberia.com', '${adminHash}'),`);
  console.log(`(2, 1, 2, 'gerente', 'gerente@barberia.com', '${gerenteHash}'),`);
  console.log(`(3, 1, 3, 'empleado', 'empleado@barberia.com', '${empleadoHash}'),`);
  console.log(`(4, 2, 4, 'recepcion', 'recepcion@barberia.com', '${recepcionHash}')`);
  console.log(`ON CONFLICT (username) DO NOTHING;`);
}

generatePasswords().catch(console.error);

