import passwordGen from 'password-generator';

export function generatePassword() {
  let password = '';
  const pattern = /(?=.*[0-9])(?=.*[a-zA-Z!@#$%^&*])/;
  while (!pattern.test(password)) {
    password = passwordGen(
      8, 
      false, 
      /[\d\W\w\p]/
    );
  }
  return password
}