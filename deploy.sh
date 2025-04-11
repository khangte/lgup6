read -p "커밋 메시지를 입력하세요: " commit_message

timestamp = $(date "+%Y-%m-%d %H:%M:%S")

git add .
git commit -m "${commit_message} - ${timestamp}"
git push
