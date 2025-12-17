import streamlit as st

st.title("🎵 한국어 노래 가사 분석 & 번역기")
st.write("가사를 입력하면 **전체 번역**과 **단어별 품사 분석**을 동시에 수행합니다.")

from konlpy.tag import Okt
import pandas as pd
from googletrans import Translator

# 페이지 설정
st.set_page_config(page_title="K-Pop 가사 분석기", layout="wide", page_icon="🎵")

# 형태소 분석기 및 번역기 초기화
okt = Okt()
translator = Translator()

# --- 사이드바: 설정 ---
st.sidebar.header("설정")
target_language = st.sidebar.selectbox("번역할 언어 선택", ["English", "Japanese", "Chinese (Simplified)"], index=0)
lang_code = {'English': 'en', 'Japanese': 'ja', 'Chinese (Simplified)': 'zh-cn'}

# --- 메인 영역 ---
lyrics_input = st.text_area("노래 가사를 입력하세요:", height=250, placeholder="여기에 한국어 가사를 붙여넣으세요...")

if st.button("분석 및 번역 시작"):
    if lyrics_input.strip():
        # 레이아웃 나누기 (왼쪽: 번역, 오른쪽: 단어 분석)
        col1, col2 = st.columns(2)

        import streamlit as st
        import pandas as pd
        from googletrans import Translator

        # Konlpy는 실행 환경에 따라 JVM(Java)이 필요하거나 패키지가 없을 수 있으므로
        # 안전하게 import 및 초기화를 수행합니다.
        konlpy_available = True
        konlpy_error = None
        try:
            from konlpy.tag import Okt
            try:
                okt = Okt()
            except Exception as _e:
                konlpy_available = False
                konlpy_error = f"Konlpy 초기화 오류: {_e}"
                okt = None
        except Exception as e:
            konlpy_available = False
            konlpy_error = f"Konlpy import 오류: {e}"
            okt = None

        translator = None
        translator_error = None
        try:
            translator = Translator()
        except Exception as e:
            translator = None
            translator_error = str(e)

        # 페이지 설정
        st.set_page_config(page_title="K-Pop 가사 분석기", layout="wide", page_icon="🎵")

        # --- 사이드바: 설정 ---
        st.sidebar.header("설정")
        target_language = st.sidebar.selectbox("번역할 언어 선택", ["English", "Japanese", "Chinese (Simplified)"], index=0)
        lang_code = {'English': 'en', 'Japanese': 'ja', 'Chinese (Simplified)': 'zh-cn'}

        # --- 메인 영역 ---
        st.title("🎵 한국어 노래 가사 분석 & 번역기")
        st.write("가사를 입력하면 **전체 번역**과 **단어별 품사 분석**을 동시에 수행합니다.")

        lyrics_input = st.text_area("노래 가사를 입력하세요:", height=250, placeholder="여기에 한국어 가사를 붙여넣으세요...")

        if st.button("분석 및 번역 시작"):
            if not lyrics_input.strip():
                st.warning("분석할 가사를 입력해 주세요.")
            else:
                col1, col2 = st.columns(2)

                # 번역 처리
                with col1:
                    st.subheader("🌍 가사 번역")
                    if translator is None:
                        st.error("번역 기능을 초기화할 수 없습니다. 번역 기능이 비활성화되었습니다.")
                        if translator_error:
                            st.caption(translator_error)
                    else:
                        try:
                            translation = translator.translate(lyrics_input, dest=lang_code[target_language])
                            st.info(translation.text)
                        except Exception:
                            st.error("번역 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")

                # 형태소 분석 처리
                with col2:
                    st.subheader("📊 주요 단어 분석")
                    if not konlpy_available:
                        st.warning("Konlpy를 사용할 수 없어 형태소 분석이 비활성화되었습니다.")
                        if konlpy_error:
                            st.caption(konlpy_error)
                        # 간단한 대안: 공백 기준 단어 빈도 제공
                        words = [w for w in lyrics_input.split() if len(w) > 1]
                        if words:
                            freq = pd.Series(words).value_counts().rename_axis('단어').reset_index(name='빈도')
                            st.dataframe(freq, use_container_width=True)
                        else:
                            st.write("분석할 단어가 없습니다.")
                    else:
                        try:
                            morphs = okt.pos(lyrics_input, stem=True)
                            unique_words = []
                            seen = set()
                            target_pos = ['Noun', 'Verb', 'Adjective', 'Adverb']
                            for word, pos in morphs:
                                if pos in target_pos and len(word) > 1 and word not in seen:
                                    unique_words.append({'단어': word, '품사': pos})
                                    seen.add(word)

                            if unique_words:
                                df = pd.DataFrame(unique_words)
                                pos_map = {'Noun': '명사', 'Verb': '동사', 'Adjective': '형용사', 'Adverb': '부사'}
                                df['품사'] = df['품사'].map(pos_map)
                                df['사전 링크'] = df['단어'].apply(lambda x: f"https://ko.dict.naver.com/#/search?query={x}")
                                st.dataframe(df, use_container_width=True)
                            else:
                                st.write("분석할 명사, 동사, 형용사가 없습니다.")
                        except Exception as e:
                            st.error("형태소 분석 중 오류가 발생했습니다.")
                            st.caption(str(e))

                st.divider()
                st.success("✅ 분석이 완료되었습니다!")

        # 하단 안내
        st.caption("Powered by Konlpy (Okt) & Google Translate")
