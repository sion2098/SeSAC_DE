# 1. Base Image: Flink 공식 이미지 사용 (Java 기반)
FROM flink:latest

# 2. 패키지 설치를 위한 관리자 권한 부여
USER root

# 3. 필수 의존성 설치
# - python3, python3-dev: Python 환경 및 개발 헤더
# - build-essential: PyFlink-Java 간 통신(pemja) 컴파일을 위한 gcc 포함
# - default-jdk: JNI 헤더(jni.h) 포함 (빌드 시 필수)
RUN apt-get update && apt-get   install -y \
    python3 \
    python3-dev \
    build-essential \
    default-jdk \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

# 4. 패키지 매니저 uv 설치 (빠르고 효율적인 설치 지원)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 5. PyFlink 설치 (핵심 빌드 과정)
# Flink 이미지는 기본적으로 실행 전용인 JRE(/opt/java/openjdk)가 설정되어 있습니다.
# 하지만 PyFlink 설치 시에는 C/Java 브릿지 컴파일을 위해 JDK의 헤더 파일이 필요합니다.
# 따라서 설치 명령어 실행 중에만 JAVA_HOME을 JDK 경로(/usr/lib/jvm/default-java)로 임시 지정합니다.
RUN JAVA_HOME=/usr/lib/jvm/default-java \
    uv pip install --system --break-system-packages apache-flink

# 6. 기본 사용자(flink)로 권한 복귀
USER flink

WORKDIR /opt/flink