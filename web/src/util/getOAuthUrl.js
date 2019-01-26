export default function getOAuthUrl(redirectUri){
  const url = 'https://accounts.google.com/o/oauth2/v2/auth?'
  const client_id = 'client_id=590358208782-7q7p2drn12lkrd6dnojr8mqfaib1a8va.apps.googleusercontent.com'
  const response_type = 'response_type=token';
  const scope = 'scope=https://www.googleapis.com/auth/cloud-platform';
  const redirect_uri = `redirect_uri=${redirectUri}`;
  const final = `${url}${client_id}&${response_type}&${scope}&${redirect_uri}`;
  return final;
}
