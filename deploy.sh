read -p "커밋 메시지를 입력하세요: " commit_message

current_time=$(TZ = Asia/Seoul date "+%Y-%m-%d %H:%M:%S")

git add .
git commit -m "$current_time $commit_message"
git push
