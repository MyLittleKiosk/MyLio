/**
 * 비밀번호 유효성을 검사합니다.
 * - 8자 이상 16자 이하
 * - 영어, 숫자, 특수문자를 각각 최소 1개 이상 포함
 * @param password 검사할 비밀번호 문자열
 * @returns 유효하면 true, 그렇지 않으면 false
 */
export function verificationPassword(password: string): boolean {
  // 1. 길이 검사 (8자 이상 16자 이하)
  if (password.length < 8 || password.length > 16) {
    return false;
  }

  // 2. 영어 포함 여부 검사
  const hasLetter = /[a-zA-Z]/.test(password);

  // 3. 숫자 포함 여부 검사
  const hasNumber = /\d/.test(password);

  // 4. 특수문자 포함 여부 검사
  const hasSpecialChar = /[!@#$%^&*()_+\-=[{\]};':"\\|,.<>/?~]/.test(password);

  return hasLetter && hasNumber && hasSpecialChar;
}
