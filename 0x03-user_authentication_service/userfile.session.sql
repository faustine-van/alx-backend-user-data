INSERT INTO users (
    id,
    email,
    hashed_password,
    session_id,
    reset_token
  )
VALUES (
    id:INTEGER,
    'email:VARCHAR(250)',
    'hashed_password:VARCHAR(250)',
    'session_id:VARCHAR(250)',
    'reset_token:VARCHAR(250)'
  );