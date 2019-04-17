tar --exclude='./.vscode/' --exclude='./__pycache__/' --exclude='./backend/__pycache__/' --exclude='./backend/.virtualenvs' --exclude='./app.tar' --exclude='./frontend/repo' --exclude='./git' --exclude='./.git' --exclude='./dump' -zcvf app.tar .
scp app.tar image-matcher@analisis-imagenes.portegno.com:/home/image-matcher/imageMatcher
rm app.tar