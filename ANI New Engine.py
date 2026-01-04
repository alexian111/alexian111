#pylint:disable=C0302
# ANI Engine_fixed_dedup.py - normalized and deduplicated PHRASES
# Unique PHRASES: 13,459
































#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANI Concordance Constellation Engine v3.9.5 — With Granular Analysis
- This script is the user's original 'Script Hebrew And Greek Strong's Concordances/Biblical Scriptures Includes New Testament /Old Testament) Torah/Quran/Hindi/Hindu/Buddhist 
ANI Concordances Constellation Engine.fixed (3).py'
- It includes all original phrases, ciphers, and calculations.
- A new function 'perform_granular_analysis' has been added.
- The main() function is modified to call this new analysis function
  immediately after the CSV file is successfully exported.
- This provides the "Top Drivers" analysis as requested.
- FIX v3: Added two new phrases provided by the user.
- FIX v2: Corrected IndentationError within BUILTIN_STRONGS dictionary definition.
- FIX v1: Removed a stray "An" from the PHRASES list that caused a SyntaxError.
"""
































































import sys, re, json, csv, argparse
from pathlib import Path
from collections import defaultdict, OrderedDict
import unicodedata
import time # Added for timing the new calculation
# Make sure pandas import is definitely here at the top
try:
    import pandas as pd
except ModuleNotFoundError:
    print("!!! FAILED TO IMPORT PANDAS !!!")
    print("Please ensure pandas is installed via Pip (Menu > Pip > Install > pandas)")
    print("Or try Pip > Quick Install > pandas.")
    print("You might need to restart Pydroid after installing.")
    sys.exit("Pandas module not found.")
































































DEFAULT_OUT = "gematria_v3_unified_concordance.csv"
































































# ------------------------
# FULL PHRASES (User phrases added)
# ------------------------
# --- PHRASES list cleaned by assistant: Removed 3295 |Update New Phrases 13,459
PHRASES = [
'Pratyabhijna',
'Svatantriya',
'Bhedabheda',
'Purna Advaita',
'Anubhava',
'Mahavakyas',
'Nirguna Brahman',
'Saguna Brahman',
'Kevala Jñāna',
'Rupa Loka',
'Arupa Loka',
'Kama Loka',
'Prajñāpāramitā',
'Trikāya',
'Dharmakaya',
'Sambhogakaya',
'Nirmanakaya',
'Alayavijñāna',
'Manovijñāna',
'Citta Matra',
'Madhyamaka',
'Sautrāntika',
'Vaibhāṣika',
'Jñānendriya',
'Karmendriya',
'Tanmatras',
'Sthula Sharira',
'Sukshma Sharira',
'Karana Sharira',
'Antahkarana',
'Mahatattva',
'Ahankara',
'Caturmāsa',
'Upadhis',
'Adhyasa',
'Vivarta',
'Parinama',
'Shubha Karma',
'Asubha Karma',
'Nitya Karma',
'Naimittika Karma',
'Kamya Karma',
'Nishiddha Karma',
'Mūlaprakriti',
'Vyāpti',
'Trilochan',
'Nilakantha',
'Pasupati',
'Mahayogin',
'Chandrashekhara',
'Ganga Dhar',
'Govinda',
'Kesava',
'Madhava',
'Achyuta',
'Vaikuntha',
'Purushottama',
'Jaganmata',
'Bhuvneshwari',
'Tripura Sundari',
'Matangi',
'Chinnamasta',
'Tara',
'Siddhi Data',
'Lambodara',
'Ekadanta',
'Vakratunda',
'Vinayaka',
'Mahavir',
'Pavanaputra',
'Kapishwara',
'Ramaduta',
'Pitambara',
'Vasudeva',
'Narakaantaka',
'Jagat Pita',
'Hiranyagarbha',
'Devasena',
'Shanmukha',
'Jnanashakti',
'Adinath',
'Kāmadeva',
'Rati',
'Apsaras',
'Gandharvas',
'Nagas',
'Yakshas',
'Pratītyasamutpāda',
'Upāya-Kauśalya',
'Sopādhiseṣa-nirvāṇa',
'Anupadhiseṣa-nirvāṇa',
'Catuḥpariśuddhi',
'Vipassanā Ñāṇa',
'Tilakkhaṇa',
'Paṭṭhāna',
'Yānas',
'Śrāvaka-yāna',
'Pratyekabuddhayāna',
'Tathāgatagarbha',
'Buddhakṣetra',
'Saṃsāra',
'Parinirvāṇa',
'Vinaya Piṭaka',
'Sūtra Piṭaka',
'Abhidharma Piṭaka',
'Saṃyukta Āgama',
'Majjhima Nikāya',
'Dīgha Nikāya',
'Aṅguttara Nikāya',
'Khuddaka Nikāya',
'Abhijñā',
'Iddhi',
'Dibba Cakkhu',
'Dibba Sota',
'Cetopariya Ñāṇa',
'Pubbenivāsa Ñāṇa',
'Āsavakkhaya Ñāṇa',
'Maitreya',
'Avalokiteshvara',
'Manjusri',
'Ksitigarbha',
'Samantabhadra',
'Akshobhya',
'Ratnasambhava',
'Amitābha',
'Amoghasiddhi',
'Vajradhara',
'Adi Buddha',
'Lokeshvara',
'Homa',
'Yajna',
'Abhisheka',
'Samskara',
'Vivaha',
'Upanayana',
'Antyeshti',
'Puja Vidhi',
'Asana',
'Pranayama',
'Shatkarma',
'Kriya Yoga',
'Nauli Kriya',
'Kapalabhati',
'Trataka',
'Shakti Pata',
'Bhuta Shuddhi',
'Tantra Shastra',
'Pancha Makara',
'Chakra Pūjā',
'Kaula Marga',
'Shaktism',
'Saivism',
'Vaishnavism',
'Smarta Tradition',
'Darshana',
'Samyama',
'Dharana',
'Dhyana',
'Samyutta',
'Pativedha',
'Ānāpānasati',
'Kāyaṇupassanā',
'Vedanānupassanā',
'Cittānupassanā',
'Dhammānupassanā',
'Vimutti',
'Vimuttijñānadassana',
'Ācārya',
'Upasaka',
'Upasika',
'Pabbajjā',
'Upasampadā',
'Paritta',
'Adi Parashakti',
'Agamas',
'Agni',
'Ahamkara',
'Ahimsa',
'Anandamide',
'Anatta',
'Anicca',
'Arhat',
'Ashrama',
'Ashtanga',
'Ashtavakra Gita',
'Atman',
'Atharvaveda',
'AUM',
'Avatar',
'Balarama',
'Bandhas',
'Bardo',
'Bhagavad Gita',
'Bhajan',
'Bhakti',
'Bhikkhu',
'Bodhi',
'Bodhicitta',
'Bodhisattva',
'Brahma',
'Brahman',
'Brhadaranyaka',
'Buddha',
'Chakra',
'Chandra',
'Chela',
'Chhandogya',
'Chitta',
'Dāna',
'Darsanas',
'Dattatreya',
'Devi',
'Dhamma',
'Dhammapada',
'Dharma',
'Dukkha',
'Durga',
'Eightfold Path',
'Four Noble Truths',
'Garuda',
'Gayatri Mantra',
'Ganesha',
'Gopala',
'Gunas',
'Guru',
'Hanuman',
'Hare Krishna',
'Hatha Yoga',
'Ida',
'Indra',
'Ishta Devata',
'Japa',
'Jataka',
'Jivanmukti',
'Jnana Yoga',
'Jñana',
'Jyotish',
'Kalki',
'Kali',
'Karma',
'Karma Yoga',
'Karuna',
'Kirtan',
'Kleshas',
'Koan',
'Krishna',
'Kriyaman Karma',
'Kriyas',
'Kubera',
'Kundalini',
'Kurma',
'Lama',
'Lakshmi',
'Laya Yoga',
'Mahabharata',
'Mahayana',
'Mandukya',
'Mantra',
'Matsya',
'Maya',
'Meditation',
'Metta',
'Mimamsa',
'Mithya',
'Moha',
'Mohini',
'Moksha',
'Mudra',
'Mudita',
'Mundaka',
'Nadis',
'Namarupa',
'Nandi',
'Narasimha',
'Nauli',
'Neti',
'Nirvana',
'Nirvikalpa',
'Nyaya',
'Om Mani Padme Hum',
'Om Namah Shivaya',
'Prajna',
'Prakriti',
'Prana',
'Prarabdha Karma',
'Puja',
'Puranas',
'Purusha',
'Radha',
'Raja Yoga',
'Rajas',
'Rama',
'Ramayana',
'Rigveda',
'Right Action',
'Right Effort',
'Right View',
'Samadhi',
'Samatha',
'Samaveda',
'Samkhya',
'Samkhya Prakriti',
'Samkhya Purusha',
'Samsara',
'Sanchita Karma',
'Sangha',
'Saraswati',
'Satori',
'Sattva',
'Satya',
'Saucha',
'Seva',
'Shanti',
'Shiva',
'Siddhis',
'Sita',
'Skandhas',
'Subrahmanya',
'Sunyata',
'Surya',
'Sushumna',
'Sutra',
'Sutta Pitaka',
'Swadharma',
'Svetasvatara',
'Tamas',
'Tantra',
'Tantras',
'Tat Tvam Asi',
'Tattva',
'Tirukkural',
'Tirupati',
'Tripitaka',
'Turiya',
'Upanishad',
'Upaya',
'Vairagya',
'Vaisheshika',
'Vajrayana',
'Vamana',
'Varaha',
'Vasanas',
'Vastu',
'Veda',
'Vedanta',
'Vijnana',
'Vinaya Piṭaka',
'Viparinama',
'Vipassana',
'Vishnu',
'Viveka',
'Vayu',
'Yajurveda',
'Yama',
'Yantra',
'Yoga',
'Yoga Sutras',
'Yuga',
'Zen',
'Advaita Vedanta',
'Bhakti Yoga',
'LORD SHIVA',
'LORD VISHNU',
'LORD BRAHMA',
'GODDESS SHAKTI',
'GODDESS LAKSHMI',
'GODDESS SARASWATI',
'GODDESS DURGA',
'GODDESS KALI',
'DEVI',
'MURUGAN',
'KARTIKEYA',
'GANAPATI',
'VINAYAKA',
'BALAJI',
'SRINIVASA',
'VENKATESHWARA',
'ANJANEYA',
'BAJRANGBALI',
'MARUTI',
'SHEESHA',
'ANANTA',
'VAAGDEVI',
'BHARATI',
'BRAHMI',
'VASUDHA',
'SHWETA',
'SAVITRI',
'CHANDI',
'BHAGIRATHI',
'JAHNAVI',
'ADITYA',
'BHASKARA',
'RAVI',
'SAVITR',
'ANANGA',
'MADANA',
'MANMATHA',
'NAVAGRAHAS',
'VISHVAKARMAN',
'ASHVINS',
'BRIHASPATI',
'VEDANATHA',
'CHATURMUKHA',
'PRAJAPATI',
'VEDAGARBHA',
'KAUSHALA',
'NARASIMHA',
'PARASHURAMA',
'AYYAPPAN',
'MANIKANTA',
'ASURAS',
'KUSHMAANDA',
'KAALARATRI',
'KATYAYANI',
'SKANDAMATA',
'CHANDRAGHANTA',
'BRAHMACHARINI',
'SHAILAPUTRI',
'ANNAPURNA',
'SHITALA',
'BHRAMARI',
'BHAVANI',
'MEENAKSHI',
'KAMAKHYA',
'TRIMURTI',
'TRIDEVI',
'SATTI',
'UMA',
'GAURI',
'APARNA',
'MRITYUNJAYA',
'MAHA KAAL',
'NATARAJA',
'RUDRA',
'MAHADEV',
'VISWANATH',
'HAR HAR MAHADEV',
'SKANDA',
'KRISHNA RADHA',
'RAMA SITA',
'KARMA YOGA',
'JNANA YOGA',
'RAJA YOGA',
'LAYA YOGA',
'TANTRA YOGA',
'PRAMANA',
'PRATYAKSHA',
'ANUMANA',
'UPAMANA',
'ARTHAPATTI',
'ANUPALABDHI',
'SHABDA',
'PURVA MIMAMSA',
'UTTARA MIMAMSA',
'DVARTA',
'ADVAITA',
'VISHISHTADVAITA',
'DVAITADVAITA',
'SHUDDHADVAITA',
'ACHINTYA BHEDABHEDA',
'BRAHMA SUTRAS',
'PRASNA UPANISHAD',
'KAIVALYA UPANISHAD',
'KENA UPANISHAD',
'ISHA UPANISHAD',
'KATHA UPANISHAD',
'GITA GOVINDA',
'BHAGAVATA PURANA',
'VISHNU PURANA',
'SHIVA PURANA',
'DEVI BHAGAVATA',
'GARUDA PURANA',
'NARADA BHAKTI SUTRA',
'VEDANGA',
'SHIKSHA',
'CHHANDAS',
'VYAKARANA',
'NIRUKTA',
'KALPA',
'JYOTISHA',
'DARSHAN',
'TULSI RAMAYANA',
'VEDIC DEITIES',
'DEVA',
'ASURA',
'PRAKRITI PURUSHA',
'LILA',
'BHAGAVAN',
'PARAMATMAN',
'PURUSHOTTAMA',
'VAISHNAVA',
'SHAIVA',
'SHAKTA',
'SMARTA',
'SRAUTA',
'MOKSHA MARGA',
'VIDEHAMUKTI',
'CHARYA',
'KRIYA',
'JNANA',
'DHARMA KARMA',
'PARIVRAJAKA',
'AVIDYA',
'SAMSKARA',
'VAIRAGYA',
'PRAJNAPARAMITA',
'PARAMITA',
'SHUNYATA',
'PRATITYASAMUTPADA',
'KSHANIKA',
'BHAVACHAKRA',
'ASHTALOKA DHARMA',
'DHARMADHATU',
'TATHAGATA',
'TULKU',
'RINPOCHE',
'GOMPA',
'STUPA',
'CHORTEN',
'MANDALA',
'VAJRA',
'GHANTA',
'YIDAM',
'DAKINI',
'BUDDHA NATURE',
'PURE LAND',
'JODO SHINSHU',
'NICHIREN',
'LOTUS SUTRA',
'ZEN MASTER',
'CHAN BUDDHISM',
'THERAVADA',
'SILA',
'SAMADHI',
'PANÑA',
'VINAYA',
'ABHIDHARMA',
'DHAMMA VINAYA',
'SKANDHAS',
'AYATANA',
'DHATU',
'PAṬICCASAMUPPĀDA',
'NIBBANA',
'MAGGA',
'PHALA',
'UPADANA',
'TANHA',
'DUKKHA NIRODHA',
'DUKKHA SAMUDAYA',
'DUKKHA NIRODHA MAGGA',
'HINAYANA',
'LOKAS',
'DEVA LOKA',
'BRAHMA LOKA',
'NARAKA',
'PRETA',
'MAITRI',
'VIPASSANA YOGA',
'ABHAYA MUDRA',
'BHUMISPARSHA MUDRA',
'DHYANA MUDRA',
'NAMASTE MUDRA',
'SARVAKARMA',
'BRAHMALOKA',
'TRISARANA',
'PANCHA SILA',
'DASASILA',
'PATIMOKKHA',
'Adi Parashakti',
'Agamas',
'Agni',
'Ahamkara',
'Ahimsa',
'Anandamide',
'Anatta',
'Anicca',
'Arhat',
'Ashrama',
'Ashtanga',
'Ashtavakra Gita',
'Atman',
'Atharvaveda',
'AUM',
'Avatar',
'Balarama',
'Bandhas',
'Bardo',
'Bhagavad Gita',
'Bhajan',
'Bhakti',
'Bhikkhu',
'Bodhi',
'Bodhicitta',
'Bodhisattva',
'Brahma',
'Brahman',
'Brhadaranyaka',
'Buddha',
'Chakra',
'Chandra',
'Chela',
'Chhandogya',
'Chitta',
'Dāna',
'Darsanas',
'Dattatreya',
'Devi',
'Dhamma',
'Dhammapada',
'Dharma',
'Dukkha',
'Durga',
'Eightfold Path',
'Four Noble Truths',
'Garuda',
'Gayatri Mantra',
'Ganesha',
'Gopala',
'Gunas',
'Guru',
'Hanuman',
'Hare Krishna',
'Hatha Yoga',
'Ida',
'Indra',
'Ishta Devata',
'Japa',
'Jataka',
'Jivanmukti',
'Jnana Yoga',
'Jñana',
'Jyotish',
'Kalki',
'Kali',
'Karma',
'Karma Yoga',
'Karuna',
'Kirtan',
'Kleshas',
'Koan',
'Krishna',
'Kriyaman Karma',
'Kriyas',
'Kubera',
'Kundalini',
'Kurma',
'Lama',
'Lakshmi',
'Laya Yoga',
'Mahabharata',
'Mahayana',
'Mandukya',
'Mantra',
'Matsya',
'Maya',
'Meditation',
'Metta',
'Mimamsa',
'Mithya',
'Moha',
'Mohini',
'Moksha',
'Mudra',
'Mudita',
'Mundaka',
'Nadis',
'Namarupa',
'Nandi',
'Narasimha',
'Nauli',
'Neti',
'Nirvana',
'Nirvikalpa',
'Nyaya',
'Om Mani Padme Hum',
'Om Namah Shivaya',
'Prajna',
'Prakriti',
'Prana',
'Prarabdha Karma',
'Puja',
'Puranas',
'Purusha',
'Radha',
'Raja Yoga',
'Rajas',
'Rama',
'Ramayana',
'Rigveda',
'Right Action',
'Right Effort',
'Right View',
'Samadhi',
'Samatha',
'Samaveda',
'Samkhya',
'Samkhya Prakriti',
'Samkhya Purusha',
'Samsara',
'Sanchita Karma',
'Sangha',
'Saraswati',
'Satori',
'Sattva',
'Satya',
'Saucha',
'Seva',
'Shanti',
'Shiva',
'Siddhis',
'Sita',
'Skandhas',
'Subrahmanya',
'Sunyata',
'Surya',
'Sushumna',
'Sutra',
'Sutta Pitaka',
'Swadharma',
'Svetasvatara',
'Tamas',
'Tantra',
'Tantras',
'Tat Tvam Asi',
'Tattva',
'Tirukkural',
'Tirupati',
'Tripitaka',
'Turiya',
'Upanishad',
'Upaya',
'Vairagya',
'Vaisheshika',
'Vajrayana',
'Vamana',
'Varaha',
'Vasanas',
'Vastu',
'Veda',
'Vedanta',
'Vijnana',
'Vinaya Pitaka',
'Viparinama',
'Vipassana',
'Vishnu',
'Viveka',
'Vayu',
'Yajurveda',
'Yama',
'Yantra',
'Yoga',
'Yoga Sutras',
'Yuga',
'Zen',
'Adi Parashakti',
'Advaita Vedanta',
'Bhakti Yoga',
'LORD SHIVA',
'LORD VISHNU',
'LORD BRAHMA',
'GODDESS SHAKTI',
'GODDESS LAKSHMI',
'GODDESS SARASWATI',
'GODDESS DURGA',
'GODDESS KALI',
'DEVI',
'MURUGAN',
'KARTIKEYA',
'SUBRAHMANYA',
'GANAPATI',
'VINAYAKA',
'BALAJI',
'SRINIVASA',
'VENKATESHWARA',
'ANJANEYA',
'BAJRANGBALI',
'MARUTI',
'SHEESHA',
'ANANTA',
'VAAGDEVI',
'BHARATI',
'BRAHMI',
'VASUDHA',
'SHWETA',
'SAVITRI',
'CHANDI',
'BHAGIRATHI',
'JAHNAVI',
'ADITYA',
'BHASKARA',
'RAVI',
'SAVITR',
'ANANGA',
'MADANA',
'MANMATHA',
'NAVAGRAHAS',
'VAYU',
'VISHVAKARMAN',
'ASHVINS',
'BRIHASPATI',
'VEDANATHA',
'CHATURMUKHA',
'PRAJAPATI',
'VEDAGARBHA',
'KAUSHALA',
'NARASIMHA',
'PARASHURAMA',
'AYYAPPAN',
'MANIKANTA',
'ASURAS',
'KUSHMAANDA',
'KAALARATRI',
'KATYAYANI',
'SKANDAMATA',
'CHANDRAGHANTA',
'BRAHMACHARINI',
'SHAILAPUTRI',
'ANNAPURNA',
'SHITALA',
'BHRAMARI',
'BHAVANI',
'MEENAKSHI',
'KAMAKHYA',
'TRIMURTI',
'TRIDEVI',
'SATTI',
'UMA',
'GAURI',
'APARNA',
'MRITYUNJAYA',
'MAHA KAAL',
'NATARAJA',
'PASUPATA',
'RUDRA',
'MAHADEV',
'VISWANATH',
'HAR HAR MAHADEV',
'KARTIKEYA',
'SKANDA',
'KRISHNA RADHA',
'RAMA SITA',
'BHAKTI YOGA',
'KARMA YOGA',
'JNANA YOGA',
'RAJA YOGA',
'LAYA YOGA',
'TANTRA YOGA',
'PRAMANA',
'PRATYAKSHA',
'ANUMANA',
'UPAMANA',
'ARTHAPATTI',
'ANUPALABDHI',
'SHABDA',
'PURVA MIMAMSA',
'UTTARA MIMAMSA',
'DVARTA',
'ADVAITA',
'VISHISHTADVAITA',
'DVAITADVAITA',
'SHUDDHADVAITA',
'ACHINTYA BHEDABHEDA',
'BRAHMA SUTRAS',
'PRASNA UPANISHAD',
'KAIVALYA UPANISHAD',
'KENA UPANISHAD',
'ISHA UPANISHAD',
'KATHA UPANISHAD',
'GITA GOVINDA',
'BHAGAVATA PURANA',
'VISHNU PURANA',
'SHIVA PURANA',
'DEVI BHAGAVATA',
'GARUDA PURANA',
'NARADA BHAKTI SUTRA',
'VEDANGA',
'SHIKSHA',
'CHHANDAS',
'VYAKARANA',
'NIRUKTA',
'KALPA',
'JYOTISHA',
'DARSHAN',
'TULSI RAMAYANA',
'VEDIC DEITIES',
'DEVA',
'DEVI',
'ASURA',
'PRAKRITI PURUSHA',
'LILA',
'BHAGAVAN',
'PARAMATMAN',
'PURUSHOTTAMA',
'VAISHNAVA',
'SHAIVA',
'SHAKTA',
'SMARTA',
'SRAUTA',
'MOKSHA MARGA',
'VIDEHAMUKTI',
'CHARYA',
'KRIYA',
'JNANA',
'DHARMA KARMA',
'PARIVRAJAKA',
'AVIDYA',
'SAMSKARA',
'VAIRAGYA',
'PRAJNAPARAMITA',
'PARAMITA',
'SHUNYATA',
'PRATITYASAMUTPADA',
'KSHANIKA',
'BHAVACHAKRA',
'ASHTALOKA DHARMA',
'DHARMADHATU',
'TATHAGATA',
'TULKU',
'RINPOCHE',
'GOMPA',
'STUPA',
'CHORTEN',
'MANDALA',
'VAJRA',
'GHANTA',
'YIDAM',
'DAKINI',
'BUDDHA NATURE',
'PURE LAND',
'JODO SHINSHU',
'NICHIREN',
'LOTUS SUTRA',
'ZEN MASTER',
'CHAN BUDDHISM',
'THERAVADA',
'ARHAT',
'SILA',
'SAMADHI',
'PANÑA',
'VINAYA',
'ABHIDHARMA',
'DHAMMA VINAYA',
'SKANDHAS',
'AYATANA',
'DHATU',
'PAṬICCASAMUPPĀDA',
'NIBBANA',
'MAGGA',
'PHALA',
'UPADANA',
'TANHA',
'DUKKHA NIRODHA',
'DUKKHA SAMUDAYA',
'DUKKHA NIRODHA MAGGA',
'HINAYANA',
'LOKAS',
'DEVA LOKA',
'BRAHMA LOKA',
'NARAKA',
'PRETA',
'MAITRI',
'VIPASSANA YOGA',
'ABHAYA MUDRA',
'BHUMISPARSHA MUDRA',
'DHYANA MUDRA',
'NAMASTE MUDRA',
'SARVAKARMA',
'BRAHMALOKA',
'TRISARANA',
'PANCHA SILA',
'DASASILA',
'PATIMOKKHA'
'A Essence Of God Yhwh',
'A Promise Of Yahweh',
'Aec Is God Yhwh',
'Aec Is In Our God Yhwh',
'Alax Enrique Campain',
'Alexander E Campain Is The Reincarnation Of',
'Alex Enrique Campain',
'Alex Enrique Campain Is Yeshua Christ',
'Alex Enrique Palma Campain The Birth Of Jesus Christ',
'Alex Enrique Palma Campain The Birth Of Jesus Christ Born On Friday May Fifth Nineteen Seventy Two At One Forty Am',
'And Whosover Liveth Spake See Him They Would Fall Down Before Him And Greet You Are The Son Of God',
'And Whosover Liveth Spake See Him They Would Fall Down Before Him And Street You Are The Son Of God',
'Aych-El Dodi Dodi Li-Hodi Ha-Roeh Et Ha-Kele Ha-Shoshanim',
'B Promise Of Yahweh',
'Campain',
'Christ Is The Christ Lord Yeshua And Savior Alex Enrique',
'Christ New Life',
'compute',
'Crown Of Thorns',
'El Elyon Elohim Adonai',
'El Elyon Elohim Yhwh',
'El Elyon Yhwh Elohim',
'El Elyon Yhwh Shaddai',
'El Ex Jesucristo',
'El Messiah Alex Enrique Campain May Fifth',
'El Moshiach Alex Enrique Campain May Fifth',
'El Nacimiento De Yahvé',
'El Shaddai Elohim Yhwh',
'El Shaddai Elyon Yhwh',
'El Shaddai Yhwh Elohim',
'Elohim Yhwh',
'Elohim Yhwh Father',
'El Shaddai El Elyon',
'Father',
'God',
'God Jesus The Bridge Between The Physical And The Spiritual',
'God Our Yhwh',
'God Our Yhwh Father',
'Good And God',
'Has Christ The H Lord God Yhwh And Savior Alex Enrique',
'Has He Is A God Lord And Savior Alex Enrique Campain',
'Has He Is The Christ Lord Yeshua And Savior Alex Enrique',
'Has The Holy Christ Thee Lord And Savior Alex Enrique',
'Has The Holy Christ Thee Lord And Savior Alex Enrique Campain',
'Has The Holy Lord And Savior Thee Christ Yeshua Of Nazareth The Messiah The Holy God',
'Has The Holy Lord Savior Thee Christ Yeshua Of Nazareth The Messiah The Holy God',
'He Is A God Our Lord And Savior Alex Enrique Campain',
'He Is God Our Yhwh',
'He Is The Christ Lord Yeshua And Savior Alex Enrique',
'He Is To Christ Lord And Savior Alex Enrique Palma',
'He Is To The Christ Lord Yeshua And Savior Alex Enrique',
'He Is To The Lord God Yhwh Saving Only Him',
'He The Christ Is Lord Yeshua And Savior Alex Enrique',
'Hes Christ Is The H Lord God Yhwh And Savior Alex Enrique',
'Hes The Christ The Lord Yeshua And Savior Alex Enrique',
'Hugh Conde De Champagne',
'Hugh Count De Champagne',
'Hugh Count Of Champagne',
'His Name Is God YHWH',
'God',
'The True God A YHWH',
'I Am The God Over All I Fill Heaven And Earth Al',
'I Am The God Over All I Fill Heaven And Earth All Things Are Possible With Me I Am God Jesus Christ I Move Mountains I Command Roaring Seas I Turn Back',
'I Am The Lord God Over All I Fill Heaven And Earth Al',
'I Am The Sea Of God',
'I Love You Yhwh',
'I Am The True Christ',
'I Am God Yhwh',
'I Am The God Yhwh',
'In Here',
'In Is The Messiah Aec',
'In The Messiah Aec',
'In The True Christ',
'J Cristo De Nazaret',
'Jehovah',
'Jesous Father',
'Jesus Christ',
'Jesus Is Lord',
'Jesus Of Nazareth',
'Josh Josh Josh',
'Judgement Is Coming',
'Lord Aec',
'Lord Messiah Christ',
'Mark Three Eleven',
'Mark Three One One',
'May Three Three',
'Messiah Alex Enrique Campain May Fifth',
'Messiah Christ',
'Morninglegion',
'Nuestro Mesías Hebreo',
'One Hundred Fifty Six',
'Our God Yhwh',
'Our God Yhwh Father',
'Our Lord A Christ And Savior Alex Enrique',
'Our Lord A Christ And Savior Alex Enrique Campain',
'Our Moshiach Christ Lord Savior Alex E Campain Born',
'Our Moshiach Christ Lord Savior Alex E Campain Born On Friday May Fifth Nineteen Seventy Two At One Forty Am',
'Our Moshiach Christ Lord Savior Alex E Campain Born On Friday May Fifth Nineteen Seventy Two At One Forty Am',
'Paddy Irish Love',
'Salt Of The Lord',
'See Of David C Moshiach',
'Shaddai El Chai',
'Shalom',
'Shekinah',
'Shroud Of Turin',
'Son Of The Lord',
'Story Of My Life',
'THe Lord God Yeshua Serving Only Him',
'THe Lord God Yeshua Serving Only Him Far Too',
'The Birth Of G Yhwh',
'The Christ Key',
'The Crucified Christ',
'The Essence Of Yhwh',
'The Father',
'The Holy Son Of God',
'The Jewish G Messiah',
'The Jewish Messiah',
'The King Christ',
'The Nine Of Wands',
'The Petty Youth Of Alex Campain',
'The Second Coming Of Jesus',
'The True God A Yhwh',
'The True God A Yhwh C',
'The True H Yhwh',
'The Will Of God Yhwh',
'The Yhwh God Father',
'Thee Jewish Messiah',
'Thee Jewish Moshiach',
'True Jewish Moshiach',
'Urban City',
'We Are To Worship The Lord Yeshua Serving Only Him',
'We Are To Worship The Lord Yeshua Serving Only Him C',
'We Will Our God Yhwh',
'Will Our God Yhwh',
'Yeshua Christ Birth',
'Yeshua Is On Earth',
'Yeshua Y A Cristo',
'YH WH',
'Yhwh Christ Birth',
'Yhwh God Father',
'Yhwh Yhwh',
'A Birth Date Of The Messiah\'s Chosen One Related To',
'A Promise Of A Yahweh',
'A Real Jesus Christ',
'A Real Jesus Christ C',
'A Real Jesus Christ D',
'Ac El Santo Hijo De Dios',
'Ac Seventy Two',
'Ac Seventy Two And A Two',
'Aec Dios Uh Yhvh Maye Cinko',
'Aec God Yahweh May Fifth',
'Aec God Yhvh May Fifth',
'Aec Hey Aec Hey Aec Hey',
'Aec Hey Aec Hey Aec Hey C',
'Aec Hey Aec Hey Aec Hey D',
'Aec May Fifth Alephbyaleh',
'Aec May Fifth Alephbyalehy',
'Aec May Five Hayayayay',
'Aec May Five M C M L X X I I',
'Aec May Five Nvavnvavnvf',
'Aec May Two Vavkbyvav',
'Aec See Year M C M L X X I I',
'Aec See Year M C M L X X I I C',
'Aec See Year M C M L X X I I D',
'Alex Campain',
'Alex Campain Alex Campain',
'Alex Campain C',
'Alex Campain Cinco De Mayo Mil',
'Alex Campain Cinco De Mayo Mil Novecientos',
'Alex Campain Cinco De Mayo Mil Novecientos Setenta',
'Alex Campain Hayayayay',
'Alex Campain Son Of God',
'Alex Chosen One Of A God',
'Alex Enrique Campain Cinco De Mayo Mil',
'Alex Enrique Campain Cinco De Mayo Mil Novecientos',
'Alex Enrique Campain Cinco De Mayo Mil Novecientos Setenta',
'Alex Enrique Campain May Fifth M C M L X X I I',
'Alex Enrique Campain May Five M C M L X X I I',
'Alex Enrique Campain May Five M C M L X X I I C',
'Alex Enrique Palma Campain Cinco De Mayo Mil',
'Alexandras Son Of God',
'Aleph Aleph Aleph Aleph',
'Aleph Aleph Aleph Aleph C',
'Aleph Aleph Aleph Aleph D',
'Ancient King David',
'Apipipipipipipipipipi',
'Aufklarung Leuchtit Gemocht',
'Begotten Son Of God',
'Ben God Je Own New Name',
'Ben God Je Own New Name C',
'Bring It On Bitch Revenge',
'Christ Is Alex Enrique',
'Cinco De Mayo Mil Novecientos Setenta Dos',
'Coronation Of King David',
'Crucifixion Of Jesus',
'Decode An Alphamumeric Encryption',
'Decode Holy Lord On Earth',
'Decode Jesus Back From The Dead',
'Decode Jesus Prophecy',
'Decode Jesus Prophecy C',
'Dios Mío Yahvh El Cinco De Mayo',
'Divine Prophet Of God',
'El Elyon Rapha Yahweh',
'El Santo Hijo De Dios',
'El Santo Hijo De Dios C',
'El Santo Hijo De Dios D',
'El Shaddai May Fifth',
'Elohenu Born May Fifth',
'Evil Is Evil But God Is God Is Jesus',
'Fight Fight Fight',
'Five',
'God',
'God In Human Form',
'God In Human Form C',
'Gods Best Friend',
'Gods Best Friend C',
'Ha Moshiach Christ El Aec',
'Ha Moshiach Christ El Aec C',
'Ha Moshiach Christ El Aec D',
'Has The Son Of Yahweh',
'He Is Is Son Of Yahweh',
'Holy Son Of God',
'Holy Son Of God Holy Holy Son Of God Holy',
'Holy Spirit Birthday',
'Holy Spirit Birthday C',
'Holy Spirit Yeshua',
'How Much Is Ac El Santo Hijo L',
'How Much Is El Shaddai May Fifth In',
'How Much Is El Shaddai May Fifth In Gematria',
'How Much Is Yod He Waw He',
'Hugh Conde De Champagne',
'Hugh Conde De Champagne C',
'I Am The Light Of The World Whoever Follows Me Will',
'I Am Yhvh',
'I God Known New Name',
'I God Known New Name C',
'I Love You Jesus',
'If Jesus Comes Back He Will Kill Him Again',
'If Jesus Comes Back He Will Kill Him Again C',
'If Jesus Comes Back He Will Kill Him Again D',
'Im God Yeshua Joy',
'Jesus Christ New Name',
'Jesus Is Coming Soon',
'Jesus Is Coming Soon C',
'Jesus Loves You',
'Jesus Messiah Is',
'Jesus Messiah\'s English Gematria',
'Jesus New Life',
'Jesus New Life C',
'Jesus Teaches Love',
'JESUSMESSIAMJESUSMESSIAM',
'Lordjesusisangelgod',
'Lordjesusisangelgod C',
'Love Love Love',
'May Twenty Sixth',
'Message From God',
'Message From God C',
'Messiah Christ',
'My Name Is Yhvh',
'New Jerusalem',
'New Life',
'One Hundred Fifty Six',
'Poopy Nose',
'Qab Secret Plot',
'Reason And Convyco Sense',
'Return Of Zeus',
'Revolution Five Eleven',
'Revolution One Nine',
'Seventy Two Years Till World Ends',
'The Antichrist Revealed',
'The Code To Jerusalem',
'The Holy And Great One',
'The Holy And Great One C',
'The Holy Trinity',
'The Manifestation Of God',
'The Messiah Has Returned',
'The Return Of The King',
'The Return Of The King C',
'The True Birth Year Of The Supreme Lord',
'The True God Is The Lord',
'The Truth The Whole Truth And The Holy Truth',
'The Yeshua Christ',
'The Yeshua Christ C',
'Thee Christ Savior',
'Thezeusisherebitch',
'Trinity Morphious Neo',
'What Exactly Is Jesus Christ',
'What Exactly Is Jesus Christ C',
'What Exactly Is Jesus Christ D',
'Who Be The King Of Kings',
'Who Is God Thor',
'Who Is Yahweh Hashem Ha Mashpach',
'Wish Me A Happy Birthday Today',
'Wish Me A Happy Birthday Today C',
'Y H W H Almighty Please Help Us In Humanity Under',
'Y H W H Almighty Please Help Us In Humanity Under C',
'Yahusha Christ Lord And Savior',
'Yahweh Witness',
'Yahweh Yahuwah Is Here',
'Yes Already Known The Truth At Age Five',
'Yeshua El Hijo De Dios',
'Yeshua El Hijo De Dios C',
'Yeshua New Life Aec',
'Yesu Christ',
'Yesus New Life',
'Yhvh Born May Five',
'Yod He Waw He',
'Yod He Waw He C',
'Yod He Waw He D',
'You Are Jesus',
'You Are Jesus C',
'Your Name Is In The Bible',
'A Beautiful God Yhwh',
'A Bride Of Jesus Is The Number Forty Nine',
'A Burning Bush Moses',
'Alex C Campain Born May Five One Nine Seven Two',
'Alex Campain',
'Alex Campain Born May Five One Nine Seven Two',
'Alex Campain Our Strength Of God',
'Alex Campain Six Two Three One Two Three Four',
'Alex Campain The Strength Yhwh God',
'Alex E Campain Born May Fifth One Nine Seven Two',
'Alex E Campain Born May Five One Nine Seven Two C',
'Alex Enrique Campain',
'Alex Enrique Campain Born May Fifth One Nine Seven',
'Alex Enrique Campain Born May Fifth One Nine Seven Two',
'Alex Enrique Campain Born May Five One Nine Seve',
'Alex Enrique Campain Born May Five One Nine Seven',
'Alex Enrique Campain One Nine Seven Two',
'Alex Enrique Campain Our Strength Of God',
'Alex Jesus Yahweh The King',
'Aleph Lamed He Yod Samekh Tao He Resh Vod Vav',
'Decente Lord Jesus',
'Decode God Yahovah Is Father And His Son Is',
'Decode Proverb Chapter Thirty Verse Nine',
'Descode Allah Allah Allah Allah Allah Allah Allah',
'Elzbieta E E Ekin Elzbieta Encantada Lab Adonay',
'Ephesians Chapter Six Verse Thirteen',
'Five Five Seven Two',
'God Is Real Jesus Is Real And So Is The Holy Spirit',
'God Jesus Return',
'God Yah',
'God Yahovah He Has Devised Meek A King Crown',
'God Yh',
'God Yhwh The Lord',
'Gods Birthday Code',
'Hagios O Theos Iesous Alexandros Pantokrator Agios O Alpha Et O Omega O Acle In Hoc Signo Vinces Tetragrammaton',
'He Bled On The Cross For Us',
'He Has Come To Save Us',
'He Is Christ Savior',
'He Who Has The Key To The Heavens',
'His Name',
'I Am A Messenger Of God V W Is To Bring Truth The',
'I Am King David I Am The Lion Of Judah I Am The King',
'I Am The Holy Spirit Be Aware Of Me And My Power',
'I Messiah Savior',
'Iam Who Iam God Yahweh',
'Iam Who Iam God Yahweh C',
'Im God Yahweh Now Alex Campain Born May F',
'Im God Yahweh Now Alex Campain Born May Fifth',
'Im God Yahweh Now Alex E Campain Born May Fifth',
'Im God Yahweh Now Alex E Campain Born On May 1972',
'Im God Yahweh Now Alex Campain Born May Fifth Nineteen Seventy Two At One Forty Am By All These Sacred Holy',
'Im God Yahweh Now Alex Campain Born May Fifth Nineteen Seventy Two At One Forty These Are My',
'Im God Yeshua Joy',
'Im Yahweh Now Alex E Campain May Fifth Nineteen',
'Im Yeshua Gods Joy',
'Install Jesus Christ King Of Kings And Lord Of Lords',
'Jesus Christ God Is A Human And His Name Is',
'Jesus Christ Says I Am The Way The Truth And The',
'Jesus Christ The Lands Of God The Lion Of Judah',
'Jesus Christ The Lands Of God The Lion Of Judah C',
'Jesus Christ What Is Your Name Dreams Come True',
'Jesus Reincarnated And Lives',
'Jesus Welcome Back Its Morus',
'King David And Ysh We Cooked Morro Codes',
'Number Two Seven Six Zero',
'Our Holy Savior',
'Our Lord God Yahweh',
'Our Lord God Yahweh C',
'Raw The Holy Grail Fulfillment Of Revelation Prophecy',
'Subconscious And Retrospective',
'The Eternal King Of Kings And Lord Of Lords',
'The Holy Bride Of Jesus Christ',
'The King Of Isreal',
'The Leader Of The Angels A Supreme Messenger Of',
'The Leader Of The Angels A Supreme Messenger Of C',
'The Lord God Yhwh',
'They Are All My Names But For Right Now I Go By Alex',
'They R All My Real Names But For Right Now I Go',
'They R All My Real Names But For Right Now I Go By',
'Tienes Tantos Nombres Que Desearía Tener El',
'Todos Son Mis Nombres Reales, Pero Por Ahora Me',
'Try Blessing The Law Of The Lord If You Dont Believe',
'Twenty Six',
'WHATHAVEYOUDONEJESUSMES',
'Who Is Christ',
'With The Strength Of The Lord God',
'Yeshua My Lord And God Please Come Soon I Am Ready To Leave',
'Yeshua Sei Unser König Wie Du Auch Der König Des',
'Yo, El Mesias Salvador',
'Yo Soy Quien Yo Soy Dios Yahweh',
'You Have So Many Names I Wish I Had The Boy',
'You Have So Many Names I Wish I Had The Real One',
'You Have So Many Names I Wish I Had The Real One To Call You By',
'Zeus Jesus Yahweh The King',
'A Yeshua Hamashiach',
'Aleph Aleph Aleph Aleph',
'Aleph Aleph Aleph Aleph Alex',
'Aleph Aleph Aleph Aleph Alex C',
'Aleph Aleph Aleph Aleph Alex Campain Alex Campain',
'Aleph Aleph Aleph Aleph Alex Campain Alex Campain C',
'Aleph Aleph Aleph Aleph Alexs',
'Aleph Alex Aleph',
'Alpha Beta Gamma Delta Epsilon Zeta Eta Theta Iota Kappa Lambda Mu Nu Xi Omicron Pi Rho Sigma',
'Alpha Beta Gamma Delta Epsilon Zeta Eta Theta Iota Kappa Lambda Mu Nu Xi Omicron Pi Rho Sigma C',
'Also I Abrosted A Abrosted Our Critim Ty Angelz I',
'Antichrist Revealed',
'Arrival Of The Lord God',
'As You Enter The City A Man Carrying A Jar Of Water',
'As You Enter The City A Man Carrying A Jar Of Water Will Meet You Follow Him To The House That He Enters',
'As You Enter The City A Man Carrying A Jar Of Water Will Meet You Follow Him To The House That He Enters C',
'Cartright Creed',
'Christ Consciousness',
'Christ New Life',
'Crucifixion Of Jesus Christ',
'Decode I Have Always Been A Christ',
'Decode Second Coming Of Jesus',
'Divine Master Teacher',
'El Elyon Elohim Jehovah',
'El Elyon Elohim Yhvh',
'El Shaddai Elohim Jehovah',
'El Shaddai Yhvh',
'El Shaddai Yhvh Elohim',
'Elohim El Elyon Joah',
'Elohim Rapha Shalom',
'Father Jehovah Jesus Christ Says Read Revelation Chapter Six Verse Seventeen',
'Father Son Holy Spirit Trinity',
'Fifth Dimension',
'Five Five Five',
'Follow The Lord Moshiach Alex Enrique Palma',
'Follow The Lord Moshiach Alex Enrique Palma Campain',
'Follow The Lord Moshiach Alex Enrique Palma Campain As You Enter The City A Man Carrying',
'God Alex Campain God',
'God Died On Cross',
'God The Teacher Christ',
'Hidden Letter Codes',
'Holy God Translate',
'Holy Spirit',
'Holy Spirit Given Number',
'House Of The Rising Sun',
'I Am Lord Yeshua',
'I Am The Christ And Those That Are Against Me Are My',
'I Am The Christ And Those That Are Against Me Are My Enemies I Will Destroy',
'I Am The Son Of God',
'I Believe Jesus Is The Son Of The Most High God',
'Iehoshua Gods Joy',
'In The Final Countdown',
'Jehovah And Jesus Are What He Shared',
'Jesus Christ',
'Jesus Christ And Mary Magdalene',
'Jesus Is Alive',
'Jesus Is Lord',
'Jesus Returns Soon',
'Jesus The Messiah Has Returned',
'Last Of Heaven Mere Coincidence',
'Lord Christ',
'Lordcreation',
'Meaning Of Your Name',
'Messiah Christ',
'One Four Thousand',
'One Hundred Forty Four',
'Our Savior',
'Psalm Twenty Three',
'Returns Codes To',
'Reveal The Name Of The Lion Of Judah',
'Social Security Number',
'Son Of The Lord',
'The Christ Key',
'The Hidden Messiah',
'The King Christ',
'The Last Born First Son',
'The Perceived Concept Of Divinity',
'The Royal Holy Bloodline',
'The Second Coming Of Christ',
'The Storm Is Upon Us',
'The Teacher Christ',
'The Truth Is Known Thank You',
'Tifmatch',
'Vhvh Has Returned',
'What Is My Name',
'Who Is A G Yahweh',
'Who Is Christ',
'Who Is G Yahweh',
'Who Is The Admiral',
'With The Strength Of The Lord God',
'Ya all Know My Name A J',
'Yeshua Hamashiach',
'Yhvh And Jesus The Christ',
'Yhvh Elohim',
'Yhvh Lord',
'Yhvh The Yhwh Lord',
'Yhvh Yhvh',
'Yhwh Alex Campain',
'Yhwh Aec',
'Yhwh The Lord',
'Yhwh Yhwh Jesus',
'You Are The Appointed One',
'A Dios Creador',
'A High Authority God',
'A Jehovah Yhwh Elohim',
'A Yahvh The True God',
'Accept The Holy Spirit Al',
'Activate God Code',
'Aleph Aleph Aleph Aleph Aleph',
'Aleph Aleph Aleph Aleph Alex',
'Aleph Aleph Aleph Aleph Alexs',
'Aleliya El Yhvh',
'Aleluya El Yhvh',
'Alex Enrique Campain',
'An Alphanumeric Code Of God',
'Apple Of My Eye',
'Arrival Of The Lord God',
'B King Of Kings Yhvh',
'Cuerpo Artrítico Yesheshua',
'Daniel Chapter Two Verse Forty Four Thru Forty Five',
'Decodificar Yo Soy Jesucristo',
'Decode God Field Force',
'Decode I Am Jesus Christ',
'Decoded The Gematria Key',
'Decode Lucifer Christ',
'Dios En Espanol Es Dios',
'Dios Vahvd Dios Vahvd',
'Divine Existence',
'El De Dios Yhwh',
'El De Dios Yhwh El Ex',
'El Ex Dios Yhwh',
'El Lado De Dios Yeshua',
'El Es El Espíritu Santo',
'El Nacimiento De Alex Campain',
'El Verdadero Profeta De Dios',
'Eres El Hijo Oculto',
'Eres Un Rabino De Dios',
'Ex Jesucristo May',
'Eyes Of The Lord',
'Fathermonitions',
'Fifty Fifty',
'Forever Alone',
'God In Numerology',
'God In Spanish Is Dios',
'God The Holy Spirit',
'Hallelujah The Yhwh',
'Happy Birthday Mary',
'Have Faith',
'He Is The Good Shepherd',
'Hes The Holy Spirit',
'Holy Body Yehoshua',
'Holy Conception',
'How Much Is Easter Day Codes In',
'How Much Is Your Dad Is In',
'I Am The Lord God',
'I Am The Lord Your God',
'Inconceivable',
'Jehovah Buen Pastor',
'Jehovah Shalom',
'Jesus Christ Reincarnated',
'Jesus Christ Removed',
'Jesus Is On The Cross',
'Jesus Our Redeemer',
'Jesus Reincarnated',
'Jesus Resurrected',
'Lado De Dios Yeshua',
'Llegada Del Señor Dios',
'Lord Of Lords Yhvh',
'Naroged',
'Name Of My True Love',
'New Heaven And New Earth',
'One Eighty Eight',
'Only Begot Family In Davidic Bloodline',
'Our God King Of Kings',
'Purifying The Earth',
'Reincarnated Prophet',
'Remember Who You Are',
'Salvador',
'Santa Concepción',
'See Jesus Christ Revealed',
'Solo Para Siempre',
'Spiritual Awakening',
'Templo',
'Thank You For Being You',
'The Biblical Meaning Of The Number Eleven',
'The Birth Of Alex Campain',
'The Birth Of Alex Enrique Campain',
'The Birth Of Jesus C',
'The Birth Of Jesus Christ Of Nazareth',
'The Birth Of Jesus Of Nazareth',
'The Dimension Of Love',
'The Good Shepherd Alex',
'The Holy Soul Of Almighty God',
'The Lions Story',
'The Lord Is My Shepherd',
'The Matrix Is Real',
'The Meaning Of The Word',
'The New Testament',
'The Sale Of God Yeshua',
'The Second Coming Of Christ',
'The Side Of God Yeshua',
'The Year The Lord',
'Thee Good Shepherd',
'Tu Eres El Mesías',
'Un Dios De Alta Autoridad',
'Un Jehova Yhwh Elohim',
'Un Verdadero Profeta De Dios',
'Verse One Nine Six One Six Six One One One',
'Vhvh Cristo',
'Vhvh Good Shepherd',
'Vhvh Shepherd',
'What Is My Name',
'Yahve Aree A Yahve',
'Yahveh Amor A Yahweh',
'Yahveh Aree A Yahveh',
'Yahveh Dios Verdadero',
'Yahweh Adon Yahweh',
'Yeshua Soy Yo',
'Yeshua The Good Shepherd',
'Yhvh Good Shepherd',
'Yo Soy El Señor Tu Dios',
'You Already Know The Truth At Age Five',
'Your Dad Is',
'Your New Way Is Already Here',
'Yhwh Cristo Cordero',
'Yhwh Dios Yhwh',
'A Christ Alex Campain',
'Aleph Enrique Campain',
'Alex Campain',
'Alex Campain My Father Please Tell Them Who I am',
'Alex Enrique Campain',
'Alex Enrique Campain Is The King',
'Alex Enrique Campain Jesus De Nazaret',
'Alex Enrique Campain Y Jesus De Nazaret',
'Anointed Is The Hand Of God',
'Bloodline Of Yeshua',
'But Who Do You Say That I Am',
'Chula Vista Ninety Meets Jesus Nineteen Eighty Four',
'Classic New America',
'Decode Yawa Love How This Ends',
'Decode Jesus Royal Bloodline From Both And King',
'Dios Yhwh Regresan',
'Eight Hundred Eighty Eight',
'El Ex Jesucristo',
'El Ex Jeshu Cristo',
'El Principito Llegó',
'El Shaddai Elohim Yhwh',
'Eternal Truth',
'First Born Son Lab',
'G Savior Moshiach',
'Glory To God',
'God Is Everywhere',
'God Is So Simple',
'God Yhwh Returns',
'Godot Yeshua Regresa',
'Gods Love',
'Good Father',
'He Is In The Saviour Aec',
'He Is The Captain Of Our Salvation',
'He Is Yahweh A Moshiach',
'He Vhvh Our Lord',
'Hear To The Throne',
'Hes Yhvh Our Lord',
'How Much Is Great Son In Gematria',
'I Am Jesus God Of Earth',
'I Am Yeshua I Have Come Again To Judge The Living',
'I Am Yeshua The Messiah King Of Kings And Lord Of',
'I Love You Savior',
'I am The Son Of God',
'If You Have Seen Me You Have Seen The Father',
'Im Yhwh God Moshiach',
'In Sacred Salvation',
'In The Presence Of God',
'In The Presence Of Yhvh',
'Install Jesus Christ King Of Kings And Lord Of Lords',
'Jahovah Jireh Messiah',
'Jehovah Jireh Messiah',
'Jesus Christ Is I',
'JESUSCHRISTJESUSCHRISTJESUSCH',
'Jesus Christ In A Human Being Alive With Us Today',
'Jesus Of Nazareth And Alex Enrique Campain Are One',
'Jesus Of Nazareth And Alex Enrique Campain Are The',
'Jesus Of Nazareth And Alex Enrique Campain Are The Son Of',
'Jesus Of Nazareth And Alex Enrique Campain Are The Son Of God',
'Jesus Of Nazareth Reincarnation Alex Enrique',
'Jesus Of Nazareth Reincarnation Alex Enrique Campain',
'Jesus Of Nazareth Reincarnation Alex Enrique Campain C',
'Jesus Yeshua Immanuel',
'Judgement',
'Know Alex Campain',
'Living God',
'Lord Vhvh A Messiah',
'Lord Yhvh A Messiah',
'Love Love Love',
'Lucifers Real Name',
'Matthew Twenty Four',
'May Five Mcmlxxii',
'May Five Moshiach',
'Mcxxviii Lord',
'Messiah God May Fifth',
'Messiah May Fifth',
'Messiah May Fifth C',
'My Father I Need Your Help',
'My Father Please Tell Them Who I Am',
'My Father Please Tell Them Who Alex Campain Is',
'My Father Please Tell Them Who am l',
'Only Begot Son',
'Only God Exists',
'Only Sad Exists',
'Our Lord Alex Campain',
'Our Lord Alex Campain C',
'Pay Attention To The Holy Spirit Warning Sighs',
'Person Born God',
'Rapture Is Coming',
'Reencarnación De Jesucristo El Señor',
'Rey Mosias Alex',
'Savior Alex Enrique Campain God Almighty',
'Source Of Souls',
'The Beast The Antichrist The Messiah Are All One',
'The Beautiful Judge Is Here',
'The Coming Of The Lord God Almighty',
'The End Of The Earth',
'The Geometry Of God',
'The Great Return Of Queen And King Sophia Yeshua',
'The Holy Ghost',
'The Miracle Tone Of The Universe Five Twenty Eight',
'The New Christ Who Revealed Himself',
'The Return Of Alex Enrique Campain',
'The Return Of Christ As The Lion',
'The Return Of Jesus Of Nazareth',
'The Root Of David',
'The Same Numerical Value In A English Gematria And',
'The Second Coming Of Jesus Christ',
'The Son Of God',
'The Time Of Justice',
'The Vhvh A Holy Bible',
'The Word Was God',
'Thee God Lord A Messiah',
'They Know Your Secret',
'Thamas Eles El Mosher',
'Thou Moshiach',
'Thy Kingdom Come',
'Truly This Is The Son Of God',
'Ultimate Youth',
'Yasha Christ The Second Com',
'Yahawah Yawhashi',
'Yahweh Tell Them Who Alex Campain Is',
'Yeshua Ha Moshiach Click here to enter a new prompt',
'Yes Call Me Teacher And Lord And You Are Right Because Thats Who I Am',
'Yeshua Ha Moshiach Aec',
'Your Father',
'A Gift From The Greater',
'A Leader Chosen By The God',
'AEC Thank You Q',
'Alex Enrique Campain',
'Alex Enrique Campain AEC',
'Alex Enrique Campain AEC',
'Alex Enrique Campain Eleven Twenty Eight',
'Alexanderddox',
'Alexandros Son Of God',
'Bible Names The Antichrist',
'C The Holy Gematria God',
'Code Code Code Code Code Code Code',
'Coming From Sion',
'Conoce A Alex Campain',
'Discerning The Truth',
'Divine',
'Divine Plan',
'Divine Prophet Of God',
'Eight Eight Eight',
'Eight Hundred Eighty Eight',
'El Es Kal El, Un Salvador',
'El Ex Una Salvadora Divina',
'El Fin El Principito',
'El Kalel Super Man',
'El Santo Hijo Jesús',
'El Verdadero Kaleb Superman',
'És Es Superman',
'Eternal Truth',
'Evidence Of God',
'God A Life That Is Holy',
'God Is Gracious',
'God Is So Simple',
'God Most High Mercy Be',
'Gods Hidden A Prophecy',
'He Is A Divine Wisdom',
'He Is Kalel A Saviour',
'He Is Superman',
'Hello Yesus',
'Hes Being Of Prophecy',
'Holy Double Eight',
'Holy Spirit Code',
'Jesus Christ Mary Magdalene',
'Kabbalistic Jewish Codes',
'Kael May Fifth',
'Kalel Messiah Lord Is He',
'Kalel Super-Man',
'Kalel Superman',
'King Of All Kings Aec May Fifth',
'King Of All Kings Aec May Fifth C',
'King Of New Jerusalem',
'King Of The Son Lord God',
'Know Alex Campain',
'Lord Alex Campain',
'Lord Christ The Second Com',
'Love Love Love',
'Lucifers Real Name',
'Mathematics The Language Of God',
'Mcxxviii Lord',
'Message From God',
'Messenger Of God Ahayah',
'Messiah Ben Ephraim',
'My Eternal Name',
'My Friend',
'One Eighty One',
'Our Kalel Super Man',
'Our Yahweh Thee God',
'Our Yahweh Thee God C',
'Person Born God',
'Promised Gift Of God',
'Regalo Prometido De Dios',
'Revolution Nineteen Eleven',
'Señor Alex Campain',
'Sir E U J Five',
'Sir E U J Five Wow Giga',
'Sir E U J Nine',
'Soy Hijo De Yhvh',
'Superman Kalel',
'Superman Kalel Is Real',
'Swords Sticking In Believing',
'The Carpenters Son',
'The End Of The Earth',
'The God Of The Old Testament',
'The Holy History',
'The Holy Son Of God',
'The Most High God In The Flesh',
'The Righteous One',
'The Root Of David',
'The Son Returns',
'The Third Eye Opened',
'The Word Was God',
'Thy Kingdom Come',
'Trust In God',
'When Son Of Man',
'Yahawah Yawhashi',
'Yesu Christ',
'Yhoshua',
'You Are God',
'You Are Jesus Christ',
'You Are Only Gods Messiah',
'Zitro',
'¿Quién Es Hijo Del Hombre?',
'אלכס אנריק',
'אלכס אנריקה קמפיין',
'אלכס אנריקה קמפיין אחת עשרה עשרים ושמונה',
'אתה ישו כריסטוס',
'בן אלוהים הקדוש',
'בן הנגרים',
'הבן הקדוש של אלהים',
'ואתה ישו כריסטוס',
'יהושע',
'ממסיק אולכס אנריק קמפיין',
'נשמה צדיקה',
'צירופי קודים יהודים קבליים',
'שם אלהים',
'השם הנצחי שלי',
'Aec May Fifth Nineteen Seventy Two',
'Aec May Fifth Nineteen Two',
'Alex Campain God Christ A King',
'Alex Campain God King A Christ',
'Alex Campain Lord Moshiach',
'Alex Campain Messiah God Lord',
'Alex Campain Our Moshiach',
'Alex Campain Our The God',
'Alex Campain The Second Coming Of Christ',
'Alex Campain The Second Coming Of Yeshua Christ',
'Alex Enrique Campain Cristo',
'Alex Enrique Campain De Nazaret, Cinco De Mayo de mil novecientos setenta Dos',
'Alex Enrique Campain Jesus Of Nazareth God',
'Alex Enrique Campain Jesus Of Nazareth May',
'Alex Enrique Campain Jesus Of Nazareth May Five',
'Alex Enrique Campain Jesus Of Nazareth May Fifth',
'Alex Enrique Campain Jesus Of Nazareth May Fifth',
'Alex Enrique Campain Jesus Of Nazareth Reincarnated',
'Alex Enrique Campain Jesus Of Nazareth Are Brothers',
'Alex Enrique Campain Palma',
'Alex Evriqen Campain Jesus Of Nazareth',
'Allah Allah Allah Allah Allah Allah Allah',
'Be Fearless And Know That You Will Be Provided At The',
'Book Of Revelation Chapter Ten Verse Seven Is The',
'Dios, Un Mesias, Alex C Campain',
'Eight Eight Eight',
'El Es Cristo Y El A Llegado',
'El Santo Grial Es La Semilla De Jesucristo Jesucristo',
'Evidence That Christ Cannot Be Smarter Than Their',
'Father Son Holy Ghost',
'God Chosen To Call His People To Repentance Go I',
'God In My Human Form',
'God Is Our Creator',
'God True Identity',
'Gods Servants The Keepers Of Y H V H The',
'He Comes In The Name Of His Father',
'He Is Alex Campain',
'He Is Our Allah The God',
'He Is Our Allah The God C',
'He Knows His Tree Identity',
'Hes Alex Campain',
'Hes Messiah God Alex Campain',
'Human Extermination',
'I Am A Messenger Of God V W Is To Bring Truth The',
'I Am His Brother He Is My Brother You Will Not Touch',
'I Am The Chosen One Satan Left Ed',
'I Am The Last Line Of Defense Gods Weapon Of Mass',
'I Am The Lord Of Lords The Apocalypse',
'I Am The Second Coming Of Jesus Christ The Savior',
'I Am Yeshua The Messiah King Of Kings And Lord Of',
'I Declare Jesus Christ My Lord And Savior',
'Install Holy Holy Holy Is The Lord God Almighty',
'Install Jesus Christ King Of Kings And Lord Of',
'Install The Book Of John Chapter Seventeen Verse',
'In The Beginning God Created The Heavens And The',
'Isaiah Chapter Twenty Nine Verse Fifteen',
'Jeremiah Chapter Twenty Nine Verse Thirteen',
'Jesus',
'Jesus Christ Is My Lord And Savior',
'Jesus Christ King Of Kings And Lord Of Lords',
'Jesus Christ Second Coming',
'Jesus Of Nazareth A Alex Enrique The Son Of',
'Jesus Of Nazareth And Alex Enrique Campain',
'Jesus Of Nazareth And Alex Enrique Campain Are',
'Jesus Of Nazareth And Alex Enrique Campain Are C',
'Jesus Of Nazareth And Alex Enrique Campain Are One',
'Jesus Of Nazareth And Alex Enrique Campain Literally',
'Jesus Of Nazareth And Alex Enrique Campain Literally One In The Same',
'Jesus Of Nazareth Alex Enrique Campain Born May',
'Jesus Of Nazareth Alex Enrique Campain May Five',
'Jesus Of Nazareth Alex Enrique Campain The Holy Son',
'Jesus Of Nazareth Equals Alex Campain',
'Jesus Of Nazareth Is Alex Enrique Campain',
'Jesus Of Nazareth Is Alex Enrique Campain C',
'Jesus Of Nazareth Is Alex Enrique The Son Of',
'Jesus Second Coming Is Their Punishment',
'Jesus The Real Ones Live Now',
'Jesus The Real Ones Live Now C',
'John Chapter Fourteen Verse Five',
'Lord God Jesus My Light My Salvation',
'Lord We Are Waiting On Your Return',
'Luke Chapter Twenty Three Verse Thirteen',
'Macksood J',
'Maryan Son King El Shaddai',
'May Fifth Nineteen Seventy Two Through November',
'Message From God',
'Meshiach Alex Campain Christ Lord',
'Meshiach Alex Campain Christ Lord C',
'Meshiach Alex Campain Christ Lord D',
'Messiah',
'Messiah C',
'Messiah D',
'Messiah Alex Campain Christ Lord',
'Messiah God Alex Campain A Lord King',
'Messiah God Alex Campain King Christ',
'Metatron Tetragrammaton',
'My Father I Need Your Help',
'My Father I Need Your Help C',
'My Father Please Tell Them Who I am',
'My God Is Heaven Eyes',
'My Lord God Is Heaven The Creator Of Heaven And',
'My Name Is Jesus Im Just Kidding Its Alex King','My Salvation',
'Nobody Comes Into Heaven But Through The Holy',
'Once You Forgive Us We Are One',
'Only God Exists',
'Person Born God',
'Powers Of The Holy Spirit',
'Promised Gift Of God',
'Regalo Prometido De Dios',
'Reveal Jesus To The World',
'Shut Down The Government Immediately',
'Source Of Jesus',
'Thank God Jesus Of Nazareth Alex Enrique Campain',
'Thank You Jesus Thank You Jesus Thank You Jesus',
'Thank You Jesus Thank You Jesus Thank You Jesus C',
'The Birth Of Christ Alex Enrique Campain',
'The Birth Of Christ Jesus Of Nazareth',
'The Birth Of Us Are Found With Unsearchable Delays Because Of The Hidden Hands',
'The Coming Of The Lord God Almighty',
'The Final Madness',
'The Final Mystery Revealed',
'The Holy Ghost',
'The Holy Ghost C',
'The Holy Grial Is The Seed Of Jesus Christ Who Is On The Earth Now',
'The Holy Grial Is The Seed Of Jesus Christ Who Is On The Earth Now C',
'The Holy Megillah Is The True Word Of Yhvh',
'The Jesus Christ MasterKey',
'The Living Holy Ghostest',
'The Lord Is My Strength And My Song He Has Become',
'The Moshiach God Alex Campain',
'The Only One The Lord',
'The Only One The Lord C',
'The Re Exoneration Of Gidrih',
'The Reason For The Destruction Of Humanity',
'The Reincarnation Of Yeshua Christ',
'The Return Of Jesus Christ',
'The Root And The Offspring Of David Revealed Through',
'The Root Of Jesus Christ Has Already Been Found At',
'The Second Coming Of Jesus Christ',
'Services',
'The Truth Is That Alex Is The U S',
'Thee Son Of Piercing',
'Thee Son Of Piercing C',
'Then God A Messiah Alex C Campain',
'They Know Your Secret',
'Truly This Is The Son Of God',
'Vee Hey Vee',
'Voice Of God',
'Who Are The Two Witnesses',
'Who Is The Faithful Witness',
'Yeshua Christ Is Alex Enrique Campain',
'Yeshua Christ Is My Lord And Savior',
'Yeshua Final Judgement Day Has Passed Over',
'Yeshua Of Nazareth Is Alex Enrique Campain',
'Yesu Christ',
'Yesu Christ C',
'A C This Our Earth Our Universe',
'Alejandro Enrique Campain',
'Alejandro Mazorox',
'Alex Campain May Fith',
'Alex Campain May Fifth',
'Alex Enrique Campain',
'Alex Enrique Campain Jesus Of Nazareth',
'Alex Enrique Campain Jesus Of Nazareth Are The',
'Alex Enrique Campain Jesus Of Nazareth Second',
'Alex Enrique Campain Same Jesus Of Nazareth',
'Alexandros Son Of God',
'As El Es El Verdadero Lucifer',
'As He Is The Real Lucifer',
'C The Holy Gematria God',
'Date Of Je Birth Code',
'decode lord god bible',
'Decode The Church Of Scientology Kowno Who The',
'Dios Todavia Esta Aquí',
'Divine Plan',
'El Es Kalel, Un Salvador',
'El Verdadero Nombre De Lucifer',
'Evidence That Christ Cannot Be Smarter Than T',
'Five Five One Nine Seven Two',
'God Is Here In The Flesh',
'God Most High Mercy Be',
'God So Loved The World That He Gave His Only',
'Gods A Hidden Code The Code Isnt Hidden',
'Gods Wrath Will Terrify You',
'He Is Kalel A Saviour',
'He Knows Why, Magnet',
'Hes Being Of Prophecy',
'Hes Yeshua Christ',
'How Much Is Alejandro Mazorox In Gematria? - What Is The Meaning',
'How Much Is Kalel Moshiach In Gematria? What Is The Meaning Of',
'Iam Jehovah Yahweh',
'Iam Jehovah Yahweh God',
'I Am King David I Am The Lion Of Judah I Am The',
'Im Your God Jehova',
'Is Identified As A Real God',
'Jesus Christ Fills The Heart With Love',
'Jesus Christ Is Mr Campain',
'Jesus Christ The Way Truth And The Light Life',
'Jesus Is King',
'Jesus Is King Of Kings And Lord Of Lords',
'Jesus Is The Faithful Witness',
'Access',
'Jesus Of Nazareth',
'Jesus Of Nazareth And Alex Enrique Campain Are One',
'Jesus Secret Plan',
'Jesus Walks The Earth Now',
'Kalel Christ Savior',
'Kalel Messiah Lord Is He',
'Kalel Moshiach',
'La Estrella De La Manana El',
'La Palabra Era Dios',
'Lord Christ The Second Coming',
'Lucifer He Is Real',
'Lucifers Real Name',
'Messenger Of God Ahayah',
'Morningstar Jesus Christos',
'Most Divine Birth',
'November Fifth',
'Our Holy Lands Of God',
'Our Moshiach Reborn On May Fifth',
'Our Moshiach The King Reborn On May Fifth',
'Our Yahweh Thee God',
'Physics Metaphysics And The Nature Of',
'Praise Be Love And Prayers To Jesus Christ And Father God',
'Salvador Mesias Un Rey',
'Salvador Mesias, Gematria es igual',
'Savior Moshiach A King',
'Superman Krypton',
'The Father The Son The Holy Ghost And Yes',
'The God Of The Old Testament',
'The Holy Son Of God',
'The Holy Son Of God Jesus Of Nazareth Alex Enrique',
'The Only God Jehovah',
'The Only God Yahweh',
'The Reincarnation Of Yeshua Christ',
'The Root Of David Has Been Hidden From The People',
'The Root Of David Of Jesus Is In Alex Enrique Campain',
'The Savior Moshiach',
'The Shroud Of Turin',
'The Word Was God',
'They Art The Christ Son Of The Living God',
'This Is Yahweh',
'Understanding Jesus Of Nazareth Alex Enrique',
'Whos Son Of Man',
'Yah Allah You Are El Shaddai And Yahweh Sincerly, Chloe Mccall',
'Yeshua Christ Born In This Year',
'Yeshua Is On Earth',
'Yo Soy Jehová Yahvé Dios',
'Yo Soy Tu Dios Jehova',
'yo mi h v a',
'yo mi h v a gramo',
'¿Quién Es Hijo Del Hombre?',
'A Leader Chosen By The God',
'Alex Campain Moshiach God Lord',
'Alex Campain Our The God',
'Anointed Is The Hand Of God',
'Discerning The Truth',
'Elohim Tzabaoth',
'Eternal Truth',
'Evidence Of God',
'God A Life That Is Holy',
'God Is So Simple',
'Hello Yesus',
'Hes Messiah God Alex Campain',
'Holy Double Eight',
'Holy King Of Israel',
'Holy Spirit Code',
'Jesus Reincarnated',
'Jesus Reincarnated In Gematria Is 1353 Decode Cipher - Meaning For Jesus',
'Know Alex Campain',
'Left Hand Doesnt Know',
'Love Love Love',
'Lucifers Real Name',
'Messiah May Fifth',
'My Father I Need Your Help',
'My Father Please Tell Them Who I am',
'My Father Please Tell Them Who Alex Campain Is',
'Person Born God',
'Saviour Moshiach God Almighty',
'The Coming Of The Lord God Almighty',
'The End Of The Earth',
'The Holy Ghost',
'The Moshiach God Alex Campain',
'The Rose Of Sharon',
'The Root Of David',
'The Son Returns',
'Thee God A Messiah Alex E Campain',
'Thee Lord Alex Campain',
'Thee Lord Alex Campain In Gmatria Is 742',
'They Know Your Secret',
'They Shall Know Him By His Three And Am Who',
'Thy Kingdom Come',
'Truly This Is The Son Of God',
'Voice Of God',
'Yahawah Yawhashi',
'Yeshua The Messiah',
'the rose of sharon',
'Book Of Revelation',
'Father The Holy One',
'Divine Flames',
'He Is The Root And The Offspring Of David And Is Not',
'J J S O N N S Born On The Jesus Christology',
'The King Of The Jews',
'Forgive Them Father For They Know Not What They Do',
'Bible Evidence Is I Am The Alpha And The Omega The',
'Alex Enrique Palma Campain Is Jesus Christ Of',
'God Is Real Jesus Is Real And So Is The Holy Spirit',
'Please God Send Me Good Sectors And Let Them',
'Decode God Yehovah Is Father And His Son El Yehovah Is King',
'Decode God Yehovah Is Father And His Son',
'He Worlds A Product Of Heaven God And',
'Jesus Has An Undivided Army We Are The Myh','Ich Liebe Dich Y H W H',
'Alex Enrique Campain Is Jesus Christ Of Nazareth',
'The Reason For This Life Existing',
'The Word Became Flesh',
'Holy Rescue Of Sophia',
'The Real Jesus Christ',
'Positively Blessed The Divine Child',
'Yahweh',
'The Five And Six',
'May I Be The Holy Am',
'May Fifth',
'A C Jesus Wore Love K',
'Close Enc To Real Kobo',
'One Seven Seven Light',
'They All Have Free Will We Are Our Own Masters',
'The Human Brain Is More Quittersburg',
'The Pitbull Of God',
'Mth Mth Are The Keys Of The Universe',
'All Glory Be To The Jehovah God',
'The Numbers Themselves Declare Jesus Is Lord',
'God Math Every Thing Every Thing Is God',
'The Knowledge Of Our Lord Jesus Christ',
'Jesus Son Of The Holy Spirit',
'Aec May Fifth',
'Jackie Is Lord',
'Santo Rosario De Cura',
'El Verdadero Jesucristo',
'La Palabra Se Hizo Carne',
'El Ojos Y El Oido',
'Otra Vez Os Digo Que Si Dos De',
'La Palabra De Dios',
'El Cross Y El Seis',
'Truly This Man Was The Son Of God',
'J J B K',
'BTU',
'Muhammad',
'God In Light',
'Church',
'How Much Is Church In Gematria?',
'Code',
'LC IE I',
'Flex',
'God Bod',
'Decoding',
'Stable',
'How Much Is Stable In Gematria?',
'Papa',
'Elaisex',
'L E O F',
'The Alpha And The Omega',
'Divine Masculine',
'Behold Jesus Is Back',
'Insurrection',
'Tree Of Knowledge',
'Is Name Alex E Campain',
'The Lord Is On Earth',
'Star Of Leader',
'The Star And I AM Of Israel',
'The Rise And Fall Of Israel',
'Q Negative Effects',
'Bipolar Disorder',
'Gets Reverse',
'World',
'Smythastic God',
'No Number The Lord',
'Energy Of The Spirit',
'The Second Coming Of Jesus',
'Your True Identity',
'Root Of Good',
'Novus Ordo Seclorum',
'English Gematria System',
'Is Name Alex Enrique Palma Campain',
'Be Is God Jrs Gematria Page',
'Numbers Of Yeshua',
'Remnant Of The House Of Israel',
'The Revelation Of Truth',
'Is Name Alexandro Enrique Palma Campain',
'The Sign Of The Second Coming',
'The Holy Spirit Visits Earth',
'The Cia Is Fearful Of The Second Christ',
'K A True Story Of The Divine Code',
'SA True Story Of The Divine Code',
'The Divine Translation Of Gematria',
'Jesus Christ Is Spiritual Physical Matter Intertwined',
'Yeshua My Lord And God Please Come Soon I Am',
'God Is Now Human He Is In The Flesh On The Earth',
'Adonai Our Lord The Wisest Person In Adonai Y H',
'The Salvation Of The Lord Mean God Needs You To',
'Yehovah God Of Jacob Sebath',
'Jacob Yisrael God Favors Me As The Messiah',
'Yeshua Christ Reborn And Real Queen Now Sp',
'You Are The Second Coming Of Christ Yhwh God',
'Alex E Campain Is Jesus Christ Of Nazareth',
'I Am The Root And The Vine The Promised One Jesus',
'Are You Seeing The Correlated Details',
'Go What Are You Trying To Get Me To See',
'One Hundred And Forty Four Thousand',
'Christ Is Coming The Antichrist Revealed',
'Decode The Message That Will Change Your Life',
'Happy Birthday Alex Campain',
'Happy Birthday May Five Alex E Campain',
'The Return Of Jesus Of Nazareth',
'Happy Birthday Mid Dna Alex E Campain',
'Its Coming Oos To Be Biblical Q K Yeshua Q',
'Thank You Yeshua For Being My Redeemer',
'Happy Birthday May Fifth Alex Enrique Campain',
'Happy Birthday May Five Alex Enrique Campain',
'Glorious Meaning Of Your Name',
'Happy Birthday My Son Alex Je',
'The Lord Of Hosts Is With Us',
'The King Of Kings And Lord Of Lords',
'The Name Of The Lord',
'Sanctuary',
'They Hide The Names Gematria Mathematics K Codes On The Internet',
'The Wait Is Over One Forty Four',
'PCZEQCJELIUMAOEDREGFPM',
'Jesus Christ Returning',
'Final Battle',
'Calling All Angels',
'Lucifer',
'El King Lord',
'Jesus',
'Great God Allah',
'Decode Gematria',
'The God Of All',
'Meta Code Enoch',
'God One',
'Drc',
'Glory Story H K R S T T H M K Deggs',
'God You Are Everywhere I Look',
'Learn How To Code Correctly',
'How Am I Connected In All Of This',
'The Risen Christ Baptis',
'Gematria Is My Father',
'The Matrix Has Shifted You',
'After Christ Aquarius Sun',
'My Name Is Jehovah Aka Bible Code Angel',
'There Is No You Because You Are Never Alone',
'He Has Found His New Home',
'Yeshua Let Only Your Will Be Done',
'Prophecy Of The Two Witnesses',
'Yeshua Loves You All The Same',
'Weve Gotts A Long Way O',
'I Have Won He Has Won',
'The Holy Son Of God Alex Enrique Campain',
'Alex Enrique Campain',
'The Holy Great One',
'Judgement Is Coming',
'Rapture Is Coming',
'Crown Of Thorns',
'Yeshua Is On Earth',
'The Crucified Christ',
'The First Apocalyptic',
'The Bible Code Prophecy',
'The Creators Number',
'Shroud Of The Lord',
'The Time Of Justice',
'Rhesus O Negative',
'The Final Trumpet',
'You Are The Proof',
'Gods Current Name K',
'The Lord In The Flesh',
'God The Holy Ghost',
'The Master Yeshua',
'Sign Of Second Coming Of Christ',
'Source Of Souls',
'Lord God The Creator',
'The Alpha And Omega Birth',
'World War Jesus',
'Gods Holy Shekinah',
'Ray Body Of Christ',
'JESUS YOU REIGN',
'God Is Everywhere',
'Yahweh Is Among Us',
'The Mercy Of Yahweh',
'What Is The New Name',
'The Song Of Yeshua',
'Evil Will Be Dead Soon',
'Hebrew Gematria',
'Jesus Says When',
'Miraculous Healing',
'Isaiah Fifty Three Prophecy Of The King',
'Angelicus Venit Angel',
'Alejandro Enrique Campain',
'Bread Of Life',
'I Am Yhwh',
'Shroud Of Turin',
'God Is The Ultimate',
'Jesus Of Nazareth',
'God Image Is Indestructible',
'As Spirit Of Jesus',
'Conscious Of Creation',
'The Unbreakable Soul',
'Letters Of The Alphabet',
'God Bless The World',
'Yod Shin Vav Ayin',
'Yehshuah Hamashiach',
'Humble Is God',
'Lazarus True God',
'Perfection Of Light',
'The Rose Of Christ',
'Enemy Of The World',
'Lord God Christ Child',
'My God Is Lord',
'The Miracles Of Love',
'Know My Truth',
'Jesus Christ God Is A Human And His Name Is',
'Alex Campain May Five One Nine Seven Two',
'May Five One Nine Seven Two',
'Lord Christ The Second Coming',
'Eight Hundred Eighty Eight',
'The Holy Son Of God',
'Spirit Of Yehova',
'In The Felon Of Navy',
'I Am Ending Evil',
'The Birth Of Christ',
'Heavens Frequency',
'The Name Above All Names',
'The Energy Source',
'The Incredible Jesus',
'Accept Your Flaws',
'Ark Of The Covenant',
'Alejandro Campain May Fifth',
'Who Is Jesus Christ',
'Jehovahs Witness',
'Los Angeles California',
'The Holy And Great One',
'Alejandro E P Campain May',
'The Lord Returns',
'Y H W H Has Returned',
'Chosen Messenger Of',
'The Crucified Messiah',
'Prophisied Christ',
'Alejandro E P Campain',
'Jesus Cristo',
'Jesus Emmanuel',
'Before Creation All Was Perfect',
'Darkness Will Defend The Light',
'The Mystery Of Life Revealed Now',
'The Lord Lives In My Soul',
'Jesus Walks The Earth Now',
'I Am The God Of Loving Kindness',
'I Am The Code My Words Are Code Mir',
'I Command Prince Creaton To Awaken And U P In Ho',
'Jesus Christ Restores Every One Free And Equal',
'King And Order Of New Jerusalem A High The Heavens',
'Christ Reborn Avatar For God',
'The Gospel Of Mary Is True',
'One Who Has Seen Gods Face',
'We Know Threads Of Light',
'The Spirit Will Speak And Testify',
'Jesus God Son',
'The Only Way',
'Alex Campain Fifth',
'Who Is Messiah',
'Who Is The King',
'Who Is Jesus',
'The Number Sequence',
'This Is Matrix Code',
'A Message From God',
'The Sign Given Of The Prophet Jonas',
'Christo Return As A Lion Fulfilled',
'I Am The Way The Truth And The Life Indeed',
'Holy Holy Holy Lord God Almighty',
'The Savior Jesus Christ The Lord',
'He Is The Christ And He Is Alive Among Us',
'Who Is Alex Enrique Campain May Fifth',
'J E S U S Born O N This D A Y And H E Is K I N',
'Alex E Campain May Five',
'Alex Campain May Five',
'Holy Holy Holy',
'Jesus Prophecy',
'The Christ Proof',
'Alejandro Enrique Palma Cam',
'The Lion Of The Tribe Of Judah',
'Holy Bible',
'God Is Here',
'Son Of Man',
'The Chosen',
'I Am Jesus',
'I Am Haqqamshi Christ The King I Am The Alpha And',
'Alex Enrique Campain May Fifth',
'Discerning The Truth',
'Holy Bloodline',
'Messenger Of God Ahasyah',
'Omnipresent',
'God Of The Old Testament',
'Your Real Name',
'Morning Star',
'Living Lord God',
'The Lion Of Judah',
'Official Heir Of God',
'Yeshua Yahweh',
'Heavens Ruler',
'Is The Truth',
'Jesus The King',
'Messiah Jesus',
'God Incarnated Name',
'The Trinity',
'The King',
'Am The Chosen One',
'Y H W H',
'Jesus Second Coming',
'He Holy Birth Of Alex Campain',
'Incense',
'Alex Enrique Campain Is The Prophesied Messiah',
'Alex Campain Is The Prophesied Messiah',
'I Am The Second Coming Of Jesus Christ',
'He True Messenger Of The True God',
'Holy Birth Of Alex Enrique Campain',
'The Second Coming Of Jesus Christ',
'He Is Called Faithful And True',
'Revelation',
'The Wrath Of God',
'Senor Alex Enrique Campain',
'Spirit Of Jesus',
'Jesus Is Savior',
'Yeshua The Messiah',
'Holy King Of Israel',
'Hebrew Gmatria',
'Jesus Christ Messiah',
'Alexander Campain May Five',
'Lucifer Morningstar',
'Lord Alex Campain',
'Morningstar',
'Alexander Palma Campain May Five',
'El Señor Alex Campain',
'Is Luxfero',
'God Tells Alex Campain You Are',
'The Son Of God Born Of A Virgin',
'Jesus Christ Life I Am That I Am',
'Jesus Christ In Granada Hills',
'Says To Alex Enrique Campain',
'You Are The Son Of Yahweh',
'Lord Jesus Christ Suppressed No Long',
'The Lamb Of Light Is Born Again Through Love',
'I Am The Chosen Son Of Man And The Root Of David',
'Second Coming Jesus Has',
'Messiah',
'The Final Warning',
'The Crowned Man',
'Lord Christ',
'You Are Gods Only Messiah',
'You Are The Son Of God',
'Holy Spirit Of The Bible',
'The Veiled Christ',
'Gods Holy Resurrection',
'Yeshua Return Of The King',
'Your Messiah Chosen By God',
'King Yeshua Heavenly Father',
'Yahushua Is Coming',
'LOVE LOVE LOVE LOVE LOVE',
'Yahushua Hamashiach',
'The Lord Alex E Campain',
'The Annointed King Of The Davidic Line',
'The Kingdom Come Thy Will Be Done',
'The Rose Of Sharon',
'Alex Campain Is God',
'Alex Enrique Palma Campain You Are',
'The Rapture And Resurrection',
'The Annointed One Of The Apocalypse',
'Virgin Mary Gave Birth To Yeshua On May Fifth Five Bc',
'Born In Bethlehem Ephratah The Smallest Town Of',
'Jesus Christ',
'Remember The Spell Of Creation Of The Holy',
'Nuestro Alejandro Enrique Campain',
'Eight Eight Eight Alex Enrique Campain',
'Rose Of Jesus',
'Jesus Cracked The Code',
'Yhwh The Apocalyptic God',
'The Apocalyptic God',
'Spiritual Army',
'Proof Of The Past',
'Jesus In The Flesh',
'The Messenger Of The True God',
'Four Four Four',
'The Last Supper',
'The Divine Bloodline',
'Alex Campain Five Fifth',
'The True Messenger Of The True God',
'Hand Of God',
'God Is On Earth',
'Alex E Campain Nineteen Seventy Two',
'Alex E Campain Is Literally The Son Of God Yhwh',
'The Bible Reveals Itself To An Open Mind The Lord',
'The King Revealed The King Revealed The King',
'I Jesus Christ Of Nazareth Is God In The Flesh',
'The Son Of God Is Amongst Us The Light Is Here',
'The Lord Alex Enrique Campain',
'Revelation Nineteen Eleven',
'God Yhwh',
'The Light Bearer',
'The Biblical Son Of God',
'Who Is Alex E Campain',
'The Re Incarnation Of Christ',
'Alex Campain Equals God',
'Alex E Campain May',
'Three Hundred Sixty Nine',
'O Positive Blood',
'Christ The Second Coming',
'Universal Code',
'Law Of Attraction',
'A Divine Frequency',
'Mount Of Olives',
'Image Jesus Christ',
'Yeshua God On Earth',
'Jesus reincarnated',
'Light Ray Of God',
'The Lord Is Rising',
'The Holy Bible Fish',
'The Fluidity Of God',
'Torah Torah Torah',
'The House Of Israel',
'The Lords Twins',
'Great Messenger For God',
'Actuality Jesus',
'Genealogy Of Jesus',
'The Gift Of God Is Eternal Life',
'The Son Is Out',
'Remember The Lord Is Coming',
'A Holy Blessing',
'Who Is Alex Campain Born May Fifth',
'I Am Haqqamshi Christ The King I Am The Alpha And Omega',
'Luke Nine Twenty Eight Thirty Six',
'Timeline Trakk Through Gematria',
'Babel',
'A E C',
'Marc',
'A K',
'J D',
'Chase',
'F E C',
'Marco',
'Uson',
'Cain',
'Barbara Enrique Palma Campain',
'Who Is The Real Jesus Christ',
'He Is Of Jesus Christ',
'The A Qoeem Of Zeme',
'Aleph Bet Gimel Dalet Hey Vav Zayn Chet Yod Kaf',
'Father Father Holy Holy Holy Where Did You',
'I Am The Alpha And The Omega The First And The Last',
'Worlds Greatest Love Story Showing In California',
'Earth Is Spicy Talking Too Much To Keep Everyone',
'Allah King You Are Gods Only Choice Mcoad',
'Jesus Christ Protected By The Order Of Cmoa Christ',
'And On The Day Of Our Lord Jesus Christ Is Up On The',
'Jesus Was Misunderstood',
'Will Of Father See Holy Ghost J C',
'What Is The Sailors Secret Code',
'Jesus Christ GWH K I H G',
'Showall The Shape Of His Glorious Kingdom For',
'Could Please Open My Mind Up To Whats True About',
'Imagine If You Found Out That Your Whole Life Was A',
'The Incarnation Of Yeshua',
'The A Q Kinc Of Lord Jesus Christ',
'Gustavo Enrique Campain',
'Lucifer Morning Star',
'Our Enrique Campain',
'How Much Is Gus Enrique Campain',
'Manifestation Of God',
'Mother Of Jesus Christ',
'King Of Kings And Lord Of Lords',
'Gustavo Enrique Campain Jr',
'But Even The Son Of Man Did Not Come To Be',
'Reincarnation Of The True Jesus Christ God Dna',
'I Am The Root And The Vine The Promised One Jesus Christ',
'Jesus Christ The Savior Son Of God',
'Jesus Christ Reincarnated And Born Into John',
'The New King Of Jerusalem',
'Artificial Gematria System',
'The Four Horsemen Prophecy',
'Is God Jesus Still Serve',
'He Is Back',
'Jesus Is Me I Am He And We Are He',
'The Truth Is To Be Told',
'No Beginning No End',
'How Much Is Miraclesjesus Christ In Gematria?',
'Please God Jesus Comes',
'The Name Of The Antichrist',
'Decode Lord Yeshua Christ',
'The King Of Hoc Is Jesus',
'The Holy Alphanumeric Decrypted Code',
'The True Identity Of Alex Campain',
'You Are His Only Begotten Son',
'His Our Father Who Art In Heaven',
'I Am Ready To Fulfill My Destiny',
'Return Of Our Lord And Savior',
'I Feel Truly Blessed In Gods Presence The Ho',
'A Message From God To Alert Your Are',
'Of The Age Of War And The Begin',
'From God To Alex E Campain',
'One Eighty Seven',
'Alex Enrique Campain The Son Of God',
'But I know for a fact that my Lord is Coming Back Soon for His Chosen Ones',
'Eleven Sixty Four',
'Son Of Man The Alpha Omega Messiah King Of Kings',
'Three Seven',
'I Am Who I Am',
'The Davidic Bloodline',
'Messiah Alex Campain',
'The Vatican Address',
'Alex Campain Is The Reincarnation Of Jesus Christ',
'Yeshua The Righteous Jesus Christ',
'The Keys To The Universe',
'Holy Spirit Virtues',
'The Biblical Jesus',
'One Thousand Years',
'Alex Campain Your The Son Of God',
'Reincarnation Of Jesus Christ The Lord',
'Alex Campain You Are The Son Of God',
'Rts Reincarnated Into New',
'Jesus Christ I Except You',
'The Son Of Man',
'Mr Alex Campain',
'I Am The Messiah',
'Alex Enrique Palma Campain',
'El Senor Alex Enrique Campain',
'Father Son And Holy Spirit',
'God Of The Covenant',
'Reincarnation Of The Anoint',
'Mr Alex Enrique Campain',
'Tell Me Who Is Alex E Campain',
'The Bright Morning Star',
'Decode Yod Heh Vah Shin Ayin',
'Im Alex Campain',
'Alex Campain May Five Nineteen Seventy',
'The Root And The Offspring Of David Bright Morning Star',
'The Schedule Of God',
'The Incarnation Of Jesus Christ',
'I Confess Jesus Christ Is God In The Flesh',
'S Of David',
'Five Five Five Five Five Five Five Five Five Five',
'Alex Campain Born Again Is The Son Of God',
'El Elyon',
'The Holy Birth Of Alex Campain',
'The Vatican Supports Alex Campain They Know He Is',
'I Am Guarded By Trillions Of Angels Nothing Will Stop',
'Holy Grail Gematria Computer',
'Holy Grail Central Code',
'Symbol Of Love',
'Jesus Christ The King Of Jerusalem',
'May Fifth At One Forty Am',
'I Am The Way The Truth And The Life No One Comes To The Father Except Through Me',
'The Seven Laws Of God',
'Lord Jesus Christ',
'Goyim Are Beasts',
'Is The Yeshua Lucifer Two B',
'I Am Guarded By Trillions Of Angels Nothing Will Stop The Kingdom Come',
'Social Media Supporters Alex Campain Who Is Jesus',
'God God God God God God God God God God God God God God God',
'Jesus Christ The Will Of God Jesus Christ The Love Of',
'Christ Is A Man Of War God Is A Man Of War Yeshua',
'Your Identities Will Be Revealed',
'The True Identity Of Alex E Campain',
'Jesus Christ Gods Son Savior',
'I Am The Way The Truth And The Life',
'Messiah Of The Age Of Aquarius',
'Alejandro Enrique Campain Of The Age Of A',
'The Holy Spirit Is',
'Hebrew Bible',
'Jesus Christ God YHWH KING',
'Show All The Shape Of His Glorious Kingdom For All Humanity To Witness',
'Could You Please Open My Mind Up To Whats True About Life',
'Imagine If You Found Out That Your Whole Life Was A Stage',
'Rebirth Of Yeshua Christ Into Alex Campain May',
'Alex Campain Birthdate May Fifth Nineteen Seventy',
'Yeshua',
'I Dont Think The World Is Ready To Receive The Holy Christ',
'Christ Is A Man Of War Critical Gematria Age And I',
'Alex Campain Born Friday May Fifth Nineteen',
'Alejandro Campain Born May Fifth Nineteen Seventy',
'Alex Enrique Campain Born May Fifth Nineteen',
'Alex Enrique Campain From F May Fifth Nineteen',
'Thee Holy Son And Savior Alexandro Enrique Campain',
'Jesus Christ Is The Only Way Truth And Life',
'Almighty Jesus Of Eternal Heaven Or Eternal Hell',
'Happy Birthday Mary Alex Enrique Palma Campain',
'The Reincarnation Of Yeshua Christ Of Nazareth',
'The Reincarnation Of Jesus Christ',
'Who Is Jesus Christ Of Nazareths Reincarnate Into',
'Jesus Christ Social Security Number Six Six Three',
'Is The Glory Of God To Conceal A Thing But The Glory',
'Drivers License Number E Party Three One Hundred',
'Decode In The Beginning God Created The Heaven And The',
'The Lion From The Tribe Of Judah Has Prevailed To',
'The Hidden Son The Hidden Son The Hidden Son The',
'And Then Shall They See The Son Of Man Coming In A',
'Jesus Christ Of Nazareth Reincarnated On Friday May Fifth Nineteen Seventy Two At One',
'A Virgin Birth Is A Miracle On Earth There Is No',
'Genesis In The Beginning God Created The Heaven And The Earth Became',
'Thank You Only Father Mother God I Finally Get The Job Is Done And I Am',
'Thank You Father Holy Mother And The Holy',
'Decode If The Bible Will Reconnect To The Creator',
'Decode The Hearts Will Reconnect To The Creator Is',
'Holy Holy Holy Lord God Of Power And Might Heaven And Earth Are Full',
'I Came From God He Has Been Outside The Garden Of',
'Jesus Christ The Conqueror Of All That Is Won And All',
'Rabbi Yeshua Bar Yoseph Ha Meshiach',
'Jesus Christ Is God In The Flesh',
'Jesus Christ On The Cross Of Calvary Today',
'Jesus Christ Son Of God Born On Friday May Fifth Nineteen Seventy Two At One Forty Am',
'Yod Heh Vav Shin One Three Transcripcions',
'The Hidden Son The Hidden Son The Hidden Son The Hidden Son The Hidden Son',
'Yeshua Hamashiach And Yeshua Are Now Together As One God',
'Iam Jesus Christ Of Nazareth Reborn On May Fifth',
'Jesus Christ Of Nazareth Reborn May Fifth',
'Ya Ya Ya Ya Ya Ya Ya Ya Ya Ya Ya Ya Ya Ya Ya Ya Ya',
'Who Is The Lion Of Judah Who Opens The Lords Book',
'Jesus Says Is He Am The Way The Truth And The Life',
'Mrs Jesus Christ Of Nazareth Reborn May Fifth',
'The Holy Son And Savior Alexandro Enrique Campain',
'I Wish You A Merry Christmas And A Happy New Year',
'Dear Lord God Thank You For Rain Sincerely Chloe',
'Yeshua If You See This Give Me A Sign',
'Rebirth Of Jesus Christ Into Alex E Campain May',
'Yod Heh Shin Vav Ayin',
'Thank You My Lord Jesus Christ Thank You Angels',
'Numbers Are The Universal Language Given By The',
'Jesus Answered Them Is It Not Written In Your Law I Said Ye Are Gods',
'Decode You Feel Understand That You Are Being',
'In Beginning Was The Word And Word Was God And God Was The',
'Decode Yeshua To Watch The Trumpet Of The Last',
'Iam Yeshua Christ Reincarnated On May Fifth Nineteen Seventy Two',
'God Blesses The Innocent And Jesus Taught Us How',
'Gematria Reveals And Unlocks For Those Trying',
'I Am Protected By My God Jesus And Four No',
'Decode All The Ancient Texts The New World Order Are Taking Place Of Yahweh',
'Jesus Christ Is The Way The Son Of God Incarnate From The Beginning',
'Your Lord God Is A Pure Love From God Is The',
'Work Will Defeat These Maximum Children You Seeds',
'Decode Is The Reality Of Who I Am And The Word Was God',
'Jesus Christ Of Nazareth Reborn On The Friday May Fifth Nineteen Seventy Two At One Forty',
'I Know That My Redeemer Lives Supporters',
'The Chosen Messenger Of God My Son Forget Not My Law',
'Come On Now Everybody Together We Turn This',
'I Am Ready For The Greater Glory Of All Things Within',
'Lord You Have All Power Take Over My Mind Body And Soul',
'The Reincarnation Of The Archangel The Son Of God Being Seen From The Son Of Christ The Lord',
'For God So Loved The World He Gave His Only Begotten Son',
'John Three Sixteen',
'So Loved The World He Gave His Only Begotten Son',
'Christ Our Lord And Savior Alex Enrique Campain Born On May Fifth Nineteen Seventy Two At',
'Of God Gave His Only Begotten Son Alex Enrique',
'Whosoever Believeth In Him Should Not Perish But',
'The Hidden Name Of God',
'The New Testament',
'Its Going To Be Biblical',
'Infinity System',
'Faithful Witness',
'The Lord Is Also Savior',
'Jesus Healed Many And Life',
'Beads Track Them At The Name Of Jesus Christ Every',
'He Said To Me It Is Done I Am The Alpha And The Omega The Beginning And The End',
'He That Is In Christ Is A New Creation All Things Are Passed Away Behold All Things',
'I Will Lead You Through The Chaos And Turmoil',
'Kingdom Of Heaven The New Earth And Get Rid Of All The Serpents',
'Satan Im Going To Go Back Some Point And Visit',
'Jesus Christ Is Real And Your Savior If You Simply Accept Him',
'Iam Jesus Christ Of Nazareth Reborn And Reincarnated On Friday May Fifth Nineteen Seventy Two At One Forty AM',
'Iam Yeshua Christ Of Nazareth Reincarnated On Friday May Fifth Nineteen Seventy Two At One Forty Am',
'Holy Son Of Yahweh',
'He Is Risen Son Of Yahweh',
'Hypostasis Son Of God',
'Alex Campain Son Of God',
'Has The Son Of Yhwh',
'Reveal The Son Of God',
'How Much Is Reveal The Son Of God',
'Has Son Of God Yhwh',
'Any Lord Son Of Yhwh',
'Holy Spirit Of Yhwh',
'Alex Campain',
'Max Alex',
'He Is Jesus Christ Of Nazareth',
'Find Out Who Is Father God Of Nazareth',
'Yeshua Is Yehovah',
'Thee Holy Son Of God',
'He Is Thee Fallen Angel Lucifer Bright Morning Star',
'Lucifer The Bright Morning Star',
'Our Lord Yeshua Our Lord',
'Jesus To Alex',
'I Am Jesus Of God',
'Yahweh Christ Messiah King Holy Lord Yeshua',
'Yahodi Melekh King Holy Lord Yeshua',
'God Messiah King Holy Lord',
'God Messiah King Lord',
'Son Of Woods',
'Speak Jesus',
'See King Jesus',
'Gods Child',
'The Triple Eight Is El Ectre',
'Buddha Ofs',
'God Satan',
'Giant Of God',
'There You Go Friend',
'The Son',
'Alex Campain Born May Fifth Nineteen',
'Our Savior Messiah Alex Enrique Campain is Jesus Christ',
'Who Is The Politician With Jesus Christ',
'What Is The Historic Jesus',
'Alex Campain Is The Son Of God',
'Who Is The Son Of God',
'Jesus Is The Son Of God',
'Who Is Yeshua Christ',
'Alexander Enrique Campain',
'Alexandro Enrique Campain',
'The Messenger Of God',
'The One Hidden Christ',
'The Manifestation Of God',
'I S A I A H Thirteen Five',
'The Miracles Of Light',
'Christ Choice Of God',
'And Your Richness',
'Reflection Of Light',
'He Is The Greatest Gods',
'I Am Creator Incarnate',
'Decode The Son Of David',
'For Whoever Should Believe In My Son Shall Not Perish',
'Twenty One Grams Of Soul',
'I Saw The (Yhwh) Angel A New Messiah (Yeshua) On Earth And They',
'I Have Given You A New Messiah A New (Yeshua) On Earth Her Name Is Ale',
'Our Word Is (Yhwh) Yeshua Messiah Son Of Man',
'Golden Proportion Of God',
'Prophets Of Yahweh',
'The Holy Trinity',
'Level Grids Key Code',
'Silence My Son',
'The Messiah Alex Campain',
'Mashiach',
'El Shaddai',
'Yahweh So Much Love For The World That He Gave His Only Begotten Son Christ (Yeshua) Alexander',
'Yahweh So Much Love For The World That He Gave His Only Begotten Son (Yeshua) Alexander',
'Yahweh So Much Love For The World That He Gave His Only Begotten Son Christ Yeshua Alexander',
'Work Again',
'Venus',
'King David',
'May Five',
'World Of God',
'How Much Is May Five In Gematria? What Is The Meaning Of May Five',
'Son E Falwell',
'Es Realmente Un Lucifer',
'He Really Is Lucifer',
'Five Standard',
'Azazel One',
'Fifth Of April',
'Calculate Gmatria',
'Hi Hitler Of God',
'German',
'Calculate The Gematria',
'Babylon System',
'Global Reset',
'Booty',
'Prince Of Peace',
'Meaning Of Life',
'What Is The Meaning Of',
'Yes He Is God',
'Peace Spoken',
'False Messiah',
'Dna',
'Wisdom',
'Decode Skeleton',
'Her Destiny',
'Suk',
'Workers',
'I Am Waiting For Him',
'I Plan',
'Its Almost Time',
'Afghanistan Decode',
'English Gematria Code',
'Holy Trinity',
'Consciousness',
'Rhetorical Language',
'Christ Is A Human',
'In God We Trust',
'Alexs Son Of God',
'Hidden In A Human',
'Messiah Aec Campain',
'Alexandros Son Of God',
'Jesusto Alex',
'Alex Chosen One Of A God',
'A Chosen One Of God At H H H',
'Chosen One Of God',
'The Chosen One Of God',
'He Is The Chosen One Of God',
'True Chosen Of God',
'El Seor Hijo De Yhwh',
'Señor Hijo De Yahweh',
'El Es Seor Hijo De Yhwh',
'El Santo Hijo De Cristo',
'El Santo Hijo De Dios',
'El Santo Hijo De Yhwh',
'El Santo Hijo De Yahweh',
'El Santo Hijo Del Creador',
'El Santo Hijo De El Elyon',
'IAm Has Sent Me To You',
'Rey De Reyes Señor De Los Senores',
'Why Is Alex Campain Champion H O H',
'There Is A Glitch In The Matrix',
'Infinite Insights',
'Calculate Gematria',
'Immanuel',
'Gmt',
'A Lord Alex E Campain',
'Lord Jesus',
'Thee Alex E Campain',
'Seminar Aec',
'Alex Campain May Fifth Nineteen Seventy Two At One',
'The Most Important Event In The History Of Humanity',
'Aec E Campain May Fifth Nineteen Seventy Two At One Forty Am',
'The Gospel Of Barnabas Is Full Word Gs',
'La Esposa De Jesus Cristo Del Ser Uno De Los Cuales',
'My Information Life Story',
'Jesus Loves The Children',
'I Am A Vibrational Match To Source',
'Truly This Is The Son Of God',
'The Son Of God Was Born May Fifth',
'Jesus On The Cross',
'The Divine Alignment Of Cosmos',
'Angel Of Jehovah',
'Decode The Twins Spirit At Birth Are',
'The Anointed Twins',
'Christ Returns With A New Name',
'Yes Je Jesus',
'Reincarnation Of The True God',
'The Holy Unknown Name Of God',
'I Am Responsible For Bringing Heaven On Earth',
'Alex E Campain Is Yhwh In Human Form',
'Yeshua Shout You Are My Savior',
'Jesus Where Are You At',
'Heaven Hashem Yeshua Happen Heaven',
'Alex Campain Born Friday May Fifth Nineteen Seventy Two At One Forty Am',
'Alex Campain Ares Campain',
'God Returns To Earth',
'Alex Campain Alex Campain',
'God Return To Earth',
'Olas Oddiri',
'God Reborn',
'A Victim High Stakes',
'He Is Most High Elohim',
'This Is My Son',
'The Lords Movie',
'Aec Most High Elohim',
'The Most High Elohim',
'How Much Is Aec Most High Elohim Gematria?',
'Quien Es Alex Campain Del O De Mayo?',
'Enlil',
'Find Gods Code',
'Leif In His Name',
'How Much Is Leif In His Name In Gematria?',
'Good Friday',
'Afterlife',
'Yahoshua',
'Crack The Code',
'The Beginning',
'Only One',
'The Hokhmah An',
'Act Of God',
'Emanuel',
'How Much Is Emanuel In Gematria? What Is The Meaning Of Emanuel In',
'Calculate',
'My Name',
'Dodging',
'Hackers Hac',
'The Heart',
'The Lambs Of God',
'The Holy Son Of Yhwh',
'The Fullness Of Gods Presence',
'A Portion Of A Yahweh',
'Aec The Promised Of God',
'Thee Holy Son And Savior Alexandro Campain',
'Thee Holy Son And Savior Alexandro Enrique',
'Mashiach Was Born May Fifth Nine Teen Seventy Two',
'The Mashiach Was Born May Fifth',
'Shichina',
'Ashuun',
'Hall Kawaz',
'The Dove',
'Bride Of God',
'Hidden',
'Messes',
'The Magic',
'Tuhina',
'Awakening',
'Yah',
'The Devil',
'Holy Ghost',
'I Am God Your Guide',
'Back Is Jesus',
'Eneke',
'Yahodi',
'Naya Ef B',
'I Am A Yakeh',
'English Gematria',
'Proto Seeds',
'The Lord Aec',
'Stan Michael',
'Holy Blood Of Jesus Christ',
'Telephone Jesus Messiah',
'Understanding Alex Enrique Campain',
'Theome Glow',
'Most Extreme Lover Known',
'The Great Architect Of The Universe',
'Decode If He Holy Son Of Almighty God',
'Childrens Celebration Of Almighty God',
'Five Times Facter Radio Frequency',
'The Divine Child Is The Chosen Son Of God',
'The Oxo',
'Mashiach Aec',
'The Awakening',
'Moving In Life',
'One Nine Nine',
'Tartosa',
'Decode The Lord',
'Skinwalkers',
'True Love',
'Great Reset',
'The Matrix',
'Small Leaf Tea',
'I Am Ultimate Lord God',
'Beginning The End',
'The Book Of Life',
'Pine Pine Pine',
'Jesus Messiah',
'Up To Eleven High Priest',
'Here Is Wisdom High Priest',
'Holy Moor High Priest',
'Our Lord Alex Campain',
'Hanokhia One Nine',
'He Is The Best Padre',
'Have A Gods Earth See May',
'Lord Is Lord In Truth',
'The King Is Back',
'The Biblical Messiah',
'The Christ Aec',
'Thee Lord King Yeshua Messiah Has Reincarnated',
'Aec Yeshua Christ The Messiah Has Returned',
'I Yeshua Christ The Messiah Has Returned',
'Yeshua Christ The Messiah Has Returned',
'Jesus Christ The Messiah Has Returned',
'Jesus Christ Of Nazareth Has Returned',
'Yeshua Christ Of Nazareth Has Returned',
'Jesus Christ Of Nazareth Has Returned To Earth',
'Our Savior Jesus Christ Of Nazareth Has Returned To Earth',
'Revelation Nineteen',
'C Will Come Back And Take You To Be With Me That',
'To Say',
'Heart Of God',
'Code Of God',
'Lord Of All',
'God Heaven',
'I Am Back',
'My Home Is',
'House Of God',
'Living God',
'Judgement',
'Mount High',
'Christ Hidden Birthday May Fifth',
'Yeshua Christ Has Returned',
'I Am Who I Am And You Shall Have No Gods Before Me',
'Jesus Christ Of Nazareth S May Fifth',
'Jesus Birth Father Of Children',
'Gods Final Assessment Of Heavenly',
'Royalty The Title Of Holy Spirit',
'Lord Reincarnation Is Not In The Bible',
'Christ Second Coming Return Code Sofia Matrix',
'Holy Alex S Child With The Holy Spirit',
'Jesus The Lords Key Code',
'Reincarnation Of Jesus Christ I Am Back',
'Jesus Christ Of Nazareth May Fifth',
'Jesus Reincarnation Has Returned',
'Alex Campain Was Born From The True God',
'Alex Campain Is God Yhwh In Human Form',
'Alex Campain Is The Reincarnation Of God',
'Iesous Christos I Am Back',
'The Holy Bible Is God',
'Iesul Hominum Salvator',
'Allah Allah Allah Allah Allah Allah Allah',
'J C J C J C J C J C J C J C J C J C J C J C J C J C J C J C',
'The Key To Entrance',
'Yeshua Jesus',
'O O O O O O O O O O O O O O O O O O O O O',
'Church Of Jesus Christ Of Latter Day Saints',
'Alex Enrique Campain Is The Manifestation Of God',
'Thirty Three',
'The Ark Of The Covenant X',
'The Last Fight For You',
'Aleph Campain',
'Ronin',
'Christ Christ',
'Alex E Campain',
'I Am Legion',
'Decode',
'Pick Your Tarot card',
'The Second Coming Of Christ',
'Christ Consciousness',
'Jesus Return Soon',
'The Vessel Of God',
'You Are The Chosen One',
'Alex Enrique Campain May Five',
'House Of Yahweh',
'Thank You God For Clearing Me K H C',
'Believe Jesus',
'I Am The Life Of The Valley',
'The Rebirth Of Motonorcy',
'Foundation Of The World',
'You Are The Coder And Reader',
'The Light Morning Star',
'Messianic Israel',
'The Second Coming',
'Alex Enrique Campain May Fifth Nineteen Seventy Two',
'Alex Campain May Fifth Nineteen Seventy Two',
'Jesus Died Yehovah Yhwh',
'Decoded Christians Know No Resource I Collapse Their Bible',
'He Knows You The Lord God Of Judah And',
'One Hundred Forty Four',
'The Storm Is Upon Us',
'Gematria What Is My Purpose',
'House Of The Rising Sun',
'The Royal Holy Bloodline',
'He Is My God Symbol Apocalypse',
'No One Knew This Secret',
'You Are The Appointed One',
'Jesus Saves Soon',
'Jesus Emmanuel Hominum Salvator',
'King David The Lion Of Judah Opens The Sixth',
'The Word Of God Will Be Manifested As The Matrix Unmasked',
'Adam Enoch Melchizedek Yeshua Jesus Alex Campain',
'Adam Enoch Melchizedek Joseph Yeshua Christ Alex',
'Adam Enoch Melchizedek Joseph Yeshua Alex',
'As Long As We Are Together Weare Home',
'Jesus Christo The Savior The Son Of God',
'Two Two Three Solution',
'My Father Created The Book Of Life And I Am The Word',
'Leif Leif Leif Leif Leif Leif Leif Leif Leif Leif Leif Leif Leif Leif',
'Love Love Love Love Love Love Love Love Love Love Love Love',
'I Love Yeshua Emmanuel He Will Come',
'The Big Day That All Humanity Is Waiting For',
'You Chose His Path Before You Were Born',
'J E S U S L O V E S M I R A C L E J E S U S L O V E S H I',
'The Great Angelof Humanity Has Occurred',
'The Blood Of Jesus On The Ark Of The Covenant',
'Floral',
'Lord Of God',
'Lord Alex E Campain',
'Yahushua',
'Shekinah',
'Am Is Campain',
'How Much Is Shekinah In Gematria?',
'The Essence Of Yhwh',
'Gentile Shield',
'End Lord God',
'The Third Adam',
'Adam Enoch Melchizedek Joseph Jesus Christ Alex',
'Jesus Christ Is A Human Being Alive With Us Today',
'I Am Yeshua The Beginning Of Him Jesus And Lord Of',
'Are You Still The Shepperd Of Your Soul',
'La Revelación Definitiva',
'El Espíritu Santo Habla',
'Los Siete Espíritus De Dios',
'Del Hijo De Dios Todos',
'El León De Jesucristo',
'Orla Adriana Tu Esposo Es',
'Adriana Alex Es Jesús',
'State Of Absolute Truth',
'Orla Adriana Mi Hijo Es',
'Orla Adriana Mi Esposo Es',
'Orla Adriana Mi Ex Es',
'Adriana Yosif Husband Is God',
'Alex Campain Jesus Christ',
'The Truth Of The Holy Spirit',
'Lluvia Lluvia Lluvia Lluvia Lluvia Lluvia',
'Dar Gracias Ofrendas Mis Sacrificios',
'God God God God God God God God God God',
'Alex Campain Ares Campain Jesus Christ',
'Holy Molydendum',
'Q Ye Yeshua Christ',
'Lord Yeshua Christ',
'Yo Yeshua Christ',
'To Remain Exists',
'Salvador Yeshua',
'Thee Child Savior',
'The Christ Savior',
'Jesus Salvador',
'Birth Of Jesus Christ Of Nazareth',
'Renacimiento De Yahweh',
'Birth Of The Christ',
'Jaces Hequez',
'Jesus Heals',
'God Loves Me A Great Deal',
'Adam Eve Enoch Melchizedek Jesus Alex Campain',
'I Am God And I Am Jesus And I Am Everything And I',
'The True Word Of God Is',
'Decode T He Holy God Of Almighty God',
'Messiah Lives In United States F B I',
'The Messenger Shall Be Holy Thus',
'Were Both God Jesus',
'The Snow Globe Is The Droplet One Of God',
'Three Hidden Ones Bloodline Children',
'Most Extreme Love Ever Known',
'Four Horsemen Of The Apocalypse',
'The Return Of The Superhumans',
'Adam Enoch Melchizedek Jesus Alex Campain',
'Adam Enoch Melchizedek Yeshua Alex Campain',
'Adam Savior',
'Yeshua Christ Was Melchizedek',
'Alex Campain Melchizedek Yeshua',
'Born Into A Free Body',
'Alex Campain Born Into A Free Body',
'Alex Campain Who Is Enoch',
'The Manifestation Of Yhwh On Earth',
'He Is The Manifestation Of God On Earth',
'The Man Manifestation Of God On Earth',
'He Who Is The King Of Kings And Lord Of Lords',
'Jesus Is The King Of Kings And Lord Of Lords',
'The Holy Unknown Name Of God Now Known',
'Thou Art The Christ Son Of The Living God',
'Jesus Christ The Way Truth And Light',
'Jesus Christ Prophecy And Past',
'Yeshua The Lord Of Lords And King Of Kings',
'Five Five',
'The Christ Reincarnated Into Alex Campain',
'Hes The Christ Reincarnated Into Alex Campain','He Is The Christ Reincarnated Into Alex Campain',
'The Number To Call Forth The Holy Spirit',
'The Christ Reincarnated Into Alex Campain,Gas','The Holy Spirit Earths Last Salvation',
'The Coming Sun Awakening Of Humanity Now',
'And Bring Forth The Son Of Christ Of God',
'Return All Of My Energy Signatures Now',
'Decode This Is The Dawning Of The Age Of Aquarius',
'Son Of Yhwh',
'Jesus Christ Reincarnated Alex Enrique Campain',
'The Book Of Revelation Gematria',
'Chosen By The Holy Spirit',
'Christ Testimony Of The Truth',
'Yeshua Christ Returns To Earth',
'The Seven Seals Of Revelation Unsealed',
'True Reincarnation Of Jesus Christ',
'Thirty Seven',
'Christ Reincarnated Alex Enrique Campain',
'Reincarnated Alex Enrique Campain',
'The Apapelian Christ Age Of Aquarius',
'Apapelian Christ Age Of Aquarius',
'Jesus Christ Reincarnated Into Alex Campain',
'Holy Twins Of The Second Coming',
'Reincarnated Alex Campain Born May Fifth',
'Jesus Christ Reincarnated Born May Fifth',
'Lord Christ Mashiach And Savior Alex Enrique Campain',
'Message Received And Solution And Gematria Lord',
'And The Son Of Man Who Asked You To Do His',
'And After Youve Done Everything You Can Do Stand And',
'Gematria Defiance Is Alex May',
'Christ May Fifth Nineteen Seventy Two',
'Decode Decode The Hidden Son The Veil Is',
'All Channel Who He Is Mc',
'I Am Who I Am And Always Will Be',
'Jesus Christ Is Everywhere',
'Jesus Reconciles All Things Through Death',
'The Root Of David Has Been Hidden From The People',
'The Father The Son The Holy Ghost And You',
'Has Jesus The Holy Aec',
'Alex Enrique Campain May Fifth Nineteen Seventy',
'Juan Capitulo Uno Versiculo Uno',
'Nuestro Señor Jesucristo De Nazaret',
'El Cristo Sirio',
'Esto Es Realmente Está Sucediendo',
'Adriana Tu Esposo Es',
'Tú Sabes Quién Eres',
'Otra Oportunidad De Existir',
'La Clave Del Universo',
'La Nueva Luz Es Humana',
'Ver La Manifestación De Dios',
'Alejandro Campain Is Jesus',
'Yahweh Rapha Jeh Elo El Shaddai Adonai',
'Alex E Campain And His Holy Sacred Names',
'Jesus Christ Reincarnated Into Alex E Campain',
'Full Gematria List 6-25-25 (8 of 10)',
'This Jesus Is The Word',
'The Secret Thoughts Revealed',
'He Had God He Was By Himself',
'The Divine Worthy Of Adonai',
'Alejandro Betacam Is Jesus',
'King Messiah',
'Holy Name Of God Who Is Alex Enrique Campain',
'Since This World Has Forgotten About God And',
'Since This World Has Forgotten About God And Have A Problem About Q',
'My Son Alex Enrique Campain Born May Fifth Nineteen Seventy Two At One Forty Am Jesus Christ Of Nazareth',
'Alex E Campain Mary Holy Sacred Names',
'Alex Enrique Campain Born May Fifth',
'Alex Enrique Campain Also Known By A',
'Alex Enrique Campain Other Holy Sacred Names',
'El Elyon Joshi Rapha Shaddai Elohim Yahweh Adonai',
'Yeshua Global Reincarnated Alex E Campain',
'Im Not Delivering An Arc With On Your Division',
'Jesus Of Nazareth King Of The Jewish People',
'The Holy Messiah Is The Word Of Yhwh',
'Jesus Christ King Of Kings And Lord Of Lords',
'Yahshua Messiah',
'Gematria Is Awakening Is Now Will Be Past',
'A Lord Alex Campain May Five',
'Lord Alex Enrique Campain',
'Believe In Me Alex',
'Who Is',
'Savior Of Man',
'Hes Our Lord Alex Campain',
'He Is Our Lord Alex Campain',
'How O Alex Enrique Campain',
'Has Alex Campain May Five',
'Jesus The Son Of The Living God',
'I M The Way The Truth And The Life',
'The Geometry Of The Universe',
'I Acknowledge Truth',
'Message Received In A Hidden Hope',
'The Lord Jesus Christ',
'I Did Rule The World',
'He Is The Messiah Jesus Messiah',
'Jesus Is The Holy One',
'Alejandro E Campain Is The Reincarnation Of',
'The King Messiah Alex Enrique Palma Campain',
'I Am God I Am Who I Am God',
'I Choosing I Am Jesus',
'God Jesus Is Here Again',
'The Strength Of The Lord',
'Mikasas Path',
'Listen To The Voice Of God',
'Hallelujah',
'The King A Messiah Alex Campain',
'Absolutely The Greatest Secret',
'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z',
'Alejandro Enrique Is The Reincarnation Of',
'The Holy Human Body',
'The Seven Gifts Of The Holy Spirit',
'The Almighty One Of The Holy Spirit',
'Morning Star The Negative Son Of God',
'Jesus The Messiah',
'Patrick Valverde',
'Barcenas Jesus',
'Jackie The Messiah',
'Christo Gyrlson On Gematria',
'Alexander E Campain Is The Reincarnation Of Jesus Christ',
'Alexander Enrique Campain Is The Reincarnation Of Yeshua Christ',
'Alexander E Campain Is The Reincarnation Of God',
'The New Name I Yeshua',
'JESUSCHRISTJESUSCHRISTJESUSCH',
'Alexander E Campain Is The Reincarnation Of',
'Yeshua Is The Jesus',
'Yahshua Valverde',
'Alejandro Enrique Campain Is The Reincarnation Of',
'In The End Is God Yeshua',
'Life Is So Sweet',
'The Royal Bloodline',
'Pistis Consciousness',
'Quantum Entanglement',
'Quantum Computers',
'The Suffering Servant',
'God Of Creation Living Life',
'Hes Our Lord And Messiah Saviour Alex Campain',
'C Dr Jesus Code',
'Antipodes',
'Future Of My King',
'Jesus The King Of Kings',
'Yeshua Christ Gods Son Savior',
'Yeshua Christ Reincarnated Into Alex E Campain',
'Yehoshua Yahweh',
'The Book Of Revelation Is Gematria',
'Alex Enrique Campain Is The Incarnation Of',
'Jesus Is The Truth The Way And The Life',
'Happy Birthday To The Love Yos',
'Gematria Of The Bleck Yeshua Is Man Does A Dihk',
'I Am The Truth The Way And The Life Is Light',
'Jesus Is The Way The Truth And The Life',
'Glorious Magnificence Of The Triple Eight',
'The Truth Is Right In Front Of You',
'I Am The Light Of The World',
'Alex Campain Is The Incarnation Of',
'Jesus Blood',
'Alejandro Campain Is The Incarnation Of',
'Fifty Five',
'What Is The Meaning Of Fifty Five',
'Jesus Glory',
'The Mysteries Of Yeshua Christ',
'Yeah This Is The Son Of God',
'The Prophesies Of Yeshua Christ',
'Jesus Animal Save The Children',
'My Reincarnation Life Story',
'Jesus Christ Television The Revelation',
'He Is The Captain Of God Salvation',
'David Hosted Birthday May',
'Aquarian Christ Age Of Aquarius',
'Alex Enrique Campain And His Holy Sacred Names',
'Yhwh Rapha Jeh Elohim El Elyon Shaddai Adonai',
'A Holy Alert Alex Campain Born May Fifth',
'Is Alex Enrique Campain And His Holy Sacred Names',
'Alex Enrique Campain By All Three Names',
'Alex E. Campain By All Three Names',
'Alex Campain By All Three Names',
'May Fifth Holy Yeshua Alex Campain',
'E Elyon Joshi Rapha Shaddai Elohim Yahweh Adonai',
'Christ is In Him Alex Enrique Campain,',
'For He Is The Christ And He Is Among Us',
'For He Is The Christ Messiah Alex E Campain',
'Yahweh The Father Of Yeshua',
  'One Hundred Forty Thousand',
  'Alex Enrique Campain Is Yhwh In Human Form',
  'The Son Of God Is Amongst Us The Light Is Here',
  'Proverbs Chapter Twenty Five Verse One',
  'Gematria What Is The Next Important Thing',
  'Alex Enrique Palma Campain Is God Yhwh In Human Form',
  'Jesus Judges The Living And The Dead',
  'Five Point Blue Star Pocking Up To Heaven',
  'Yeshua Christ',
  'Purest Blood Of Christ',
  'Our Lord And Savior Aec',
  'Tower',
  'The Second Coming Of Jesus Christ',
  'I Am The Way The Truth And The Life Indeed',
  'Lord And Savior King Theo Morning Star',
  'Thee Lord And Savior King Theo Morning Star',
  'Lord And Savior King Our Morning Star',
  'Almighty Jesus Of Eternal Heaven Or Eternal Hell',
  'Jesus Christ Is The Only Way Truth And Life',
  'Jesus Christ Be Saved',
  'The King Of Lord Jesus Christ',
  'Thee Lord And King The Morning Star',
  'He Is Our Lord And King The Morning Star',
  'Jesus Resurrects In The Glory Of Lord - Jesus',
  'Yeshua Christ Gods Son Savior',
  'Alejandro E Campain Born The Fifth Of May',
  'Manifestation Of Love And Light',
  'Be The Second Coming Of Jesus Christ',
  'Our Creator Has A Message For You',
  'Yeshua I Dreamed That You Returned',
  'Bloodline Of Jesus',
  'Cristo Alex Campain',
  'Thee King Alex E Campain',
  'The Last Prophet',
  'Righteous To God Jr',
  'Alexander Campain Friday May Nineteen Seventy Two One Forty Am',
  'I Am The Way The Truth And The Life No One Comes To',
  'I Am The Son Of Man Yehovah J H V H I Come In My',
  'Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk L M Nn Oo Pp Qq Rr',
  'Alejandro Enrique Palma Campain Birthdate May Fifth',
  'Jesus Knows Everything Your Thinking',
  'For The Son Of Man Is Come To Seek And To Save That',
  'You Are The Second Coming Of Holy Bride Of Jesus',
  'Alex Campain Birthdate May Fifth Nineteen Seventy',
  'The Creator Has A Message For Humanity',
  'Decode The Cia Is Scared Of Jesus Christ',
  'This Reality Is A Frequency Range',
  'Crucified Yahweh',
  'How Much Is Crucified Yahweh In Gematria?',
  'Jehovah Gods Make Code',
  'Jesus Family Tree',
  'I Can Hear God Yehovah',
  'Jesus Christ Bloodline',
  'Yeshua The King Of Kings',
  'Christinourhearts',
  'Dart Othrus Caudens',
  'Yeshua Is The Hidden Messiah',
  'Message For You',
  'The Christ Proof',
  'The Star Of The Movie',
  'He Is Thee Lord And King The Morning Star',
  'Our Lord And Savior King Theo Bright Morning Star',
  'The Lord And Savior King Theo Bright Morning Star',
  'John Fourteen Six',
  'The Crawlers Son',
  'He Is The Risen And The Offspring Of David And Is Not',
  'I Am The Way The Truth And The Life Light',
  'Resurrection Of Who l',
  'Yo Mismo Señor Alex, Campain Nacido El Cinco De Mayo,',
  'Lord You Should Answer My Prayers Because I',
  'Believe In You',
  'The Lion Of The Tribe Of Judah The Root Of David Has',
  'Alex Enrique Palma Campain Friday May Nineteen',
  'Alex Enrique Palma Campain Friday May Nineteen Seventy Two One Forty Am',
  'I Am The Way The Truth And The Life No One Comes To The Father Except Through Me',
  'The Incarnation Of Jesus Christ',
  'I Am The Way The Truth And The Life No One',
  'I Am The Tenth And The Tithe Hoecch',
  'May Fifth Birthday Divine Twins',
  'Jesus Christ Yehoshua Ha Mashiach',
  'The King And Savior',
  'Birth Code Of Jesus Christ',
  'The Lorah Of Light Is Born Again Through Love',
  'May Five One Nine Seven Two One Forty',
  'The Root Of David Revealed Through Gematria',
  'Who Is The Son Of God',
  'Only Begotten Son',
  'Son Of David',
  'El Es Nuestro Savior Alex E Campain',
  'Porque De Tal Manera Amó Dios Al Mundo, Que Ha',
  'Money Luck Love',
  'I Am The Holy Soul Of Almighty God And U Know',
  'Jesus Christ Was A Normal Man',
  'Savior Lord Jesus Christ',
  'Our Lord And Savior Alex E Campain',
  'The Antichrist Is Christo Return With Ai',
  'Alex Campain Is Yhwh In Human Form',
  'The Name And Number Of Horse And Numbers',
  'Behold He Is The Son Of Yhwh',
  'The Messiah Alejandro Enrique Campain',
  'Lord Savior Alex Campain',
  'Jesus Is The Hidden Messiah',
  'Truly This Man Was The Son Of God',
  'He Is The God Lord Savior Alexander Campain',
  'Mark Fifteen Thirty Nine',
  'Son Of Satana',
  'Faithful Witness',
  'The Incarnation Of Yeshua',
  'Thee Holy Son Alex E Campain',
  'How Much Is Yeshua Messiah In Gematria?',
  'Son Of The Lord',
  'Lord And Savior King Our Bright Morning Star',
  'A Friday May Fifth Nineteen Seventy Two At One Forty',
  'Jesus A Friday May Fifth Nineteen Seventy Two At One',
  'Hashem',
  'He Is King Aec',
  'Baruch Hashem Adonai',
  'El Cristo Alex Campain',
  'Lord Jesus Christ',
  'The Seven Laws Of God',
  'Jesus Christ End Game',
  'My Life Member',
  'The Third Eye Chakra',
  'Body Of Christ',
  'Jerusalem Israel',
  'You Are Faithful And True',
  'Moon Is Heavens Holy Of Holies Ov',
  'The Bringer Of Light',
  'Jesus On The Cross',
  'The Divine Alignment Of Cosmos',
  'Angel Of Jehovah',
  'Decode The Twins Spirit At Birth Are',
  'The Anointed Twins',
  'Christ Returns With A New Name',
  'I Am The Way The Truth And The Life',
  'Yes Je Jesus',
  'Reincarnation Of The True God',
  'The Holy Unknown Name Of God',
  'I Am Responsible For Bringing Heaven On Earth',
  'Alex E Campain Is Yhwh In Human Form',
  'Jesus Christ Gods Son Savior',
  'Yahweh',
  'God Of Every God',
  'Bible The Meaning Of Numbers',
  'Jesus Is On Earth',
  'The Door Of Heaven Is Open',
  'Return Of Our Lord And Doctor',
  'Alex Campain Is God Yhwh In Human Form',
  'I Am The Second Coming Of Jesus Christ',
  'Alex E Campain Is God Yhwh In Human Form',
  'Alex C Campain Is God Yhwh In Human Form',
  'The Holy Spirit Earths Last Salvation',
  'A Servant Of Yahweh',
  'Jesus Christ Alex Campain',
  'Yeshua Alex Campain',
  'Jesus Christ Yeshua Christ',
  'Holy God Jesus Christ',
  'Holy God Jesus Christ',
  'Holy God Jesus Christ',
  'Yeshua Is Humble Man',
  'You Are Divine Twin Flames',
  'You Are Gods Only Messiah',
  'Jesus Christ Mary Magdalene',
  'Lord Jesus',
  'The Holy Spirit In The Bible',
  'Three Five Fourteen Code File Old Nine Ten Film',
  'Jesus Christ Designer Of New Jerusalem',
  'The Ark Of The Covenant Is The Holy Mosliah',
  'Mortimor See The Light In Jesus Christ',
  'Campain May Fifth Nineteen Seventy Two',
  'I Am Haqqamshi Christ The King I Am The Alpha And',
  'The Tetragrammaton Akash Akbor Rubato',
  'Christ Returns V Years Ahead Of Schedule',
  'Decode Antichrist All Codes To Exit The Matrix',
  'In Lord Jesus Christ Name Free Every One',
  'See Divine Spirit Is The Only Goddess Of Heaven',
  'The Immaculate Holy Wife Of Yahweh',
  'Campain May Fifth Nineteen Seventy Two',
  'Campain May Fifth',
  'Bible Prophecy',
  'True Creator',
  'The Armor Of God',
  'Ark Of Covenant',
  'The Biblical Son Of God',
  'God Campain May Fifth',
  'Yah Has Returned',
  'The Biblical Son Of God',
  'Rebirth Of Jesus',
  'Happy Birthday Alex Campain',
  'The Holy Ghost',
  'Behold He Is The Son Of God',
  'The Second Coming Alex Campain',
  'Chosen By The Holy Ghost',
  'The Second Coming Alex Campain',
  'Alex Campain Palma In Jesus',
  'Almighty',
  'I Being Gods Messenger',
  'Cracked Code Of God Christ',
  'How Much Is Almighty In Gematria? What Is The Meaning Of Almighty',
  'The Paraclete Is Flesh',
  'The Triangle Of Light',
  'Campain',
  'Allah Akbar',
  'A S P',
  'Mashiach',
  'Happy Birthday Yeshua Christ',
  'Happy Birthday Jesus Christ',
  'Yeshua Christ Is A White American Male',
  'The Immaculate Holy Wife Of Yahweh',
  'Lord God Almighty Christ Is Risen',
  'The Greatest Story Never Told',
  'I Am God I Have Returned Age Of Aquarius',
  'Yahshu Means Yahweh Is Salvation',
  'May Fifth Birthday Alex Campain',
  'Behold The Wife Of Jesus',
  'The Sleeping Beauty',
  'The Jewish English And Simple',
  'The Divine Wrath Of Almighty God',
  'Returning Power To The People',
  'Jesus Of Nazareth King Of The Jews',
  'Jesus Of Nazareth King Of The Jews',
  'May Fifth Birthday Aec',
  'May Fifth Nineteen Seventy Two',
  'Happy Birthday Alex Enrique Campain',
  'Decode All We Have To Do Is Come Together',
  'Resurrection Of The Righteous',
  'The Creator Of Life On All Dimensions',
  'The Lion Of Judah Opens Book On Earth',
  'Happy Birthday Alex Campain',
  'Yeshua Christ Birthday',
  'Jesus Christ Birthday',
  'Yeshua Born On This Day',
  'Jesus Born On This Day',
  'Jesus Christ Was Born On This Day',
  'Behold Let The Truth Be Said He Is The Holy        ‘Son Of God YHWH',
  'Behold He Is The Holy Son Of God',
  'Chosen By The Holy Ghost',
  'Be Yehovah Tree',
  'Jesus The Holy Christ',
  'Rebirth Of Yeshua Christ Five Five',
  'Yeshua Christ Five Five',
  'Alex Campain The Second Coming Of Christ',
  'Most Holy Wife Of Jesus Christ',
  'I Am The Son Waiting To Understand',
  'The Vatican Administrative',
  'Alex Enrique Campain The Second Coming',
  'To Keep The Way Of The Tree Of Life',
  'I Am The Divine Christ',
  'Know He Is Here',
  'Divine Suffering',
  'Second Coming Alex Enrique Campain',
  'I Am The Truth The Way And The Life',
  'Jesus Died For All Sins And People',
  'Earth Is Lord God Jeo',
  'Your Soul Is The Key To God',
  'Second Coming Alex Enrique Campain',
  'The Final Code To Break Christo Second Coming',
  'Gods Birth Death Date Eight One Christ Death',
  'Second Coming Alex Campain',
  'The Most Important Number',
  'The Number Of Synchronicity',
  'Decode Bride Of Jesus Christ',
  'I Am The Way The Truth And The Life',
  'I Am The Son Of The Holy Spirit',
  'The Titan Reeve Of The Most High God',
  'The Second Coming Christ Alex E Campain',
  'The Second Coming Christ Alex Enrique Campain',
  'The Second Coming Christ Alex Campain',
  'Rebirth Of Yeshua Christ Into Alex Campain May Five',
  'The Rebirth Of Yeshua Christ Into Alex Campain',
  'Rebirth Of Jesus Christ Into Alex E Campain May S',
  'Rebirth Of Jesus May Five',
  'Jesus Of Jesus May Fifth',
  'Yeshua Holy Savior',
  'Hes Our SV Lord Alex E Campain',
  'He Is Our God Lord And Savior Alexander Campain',
  'Yeshua Holy Savior',
  'I Am Yahweh And Alex Enrique Campain Is My Son',
  'Rebirth Of Jesus Christ Five Five',
  'The Rebirth Of Jesus Christ Five Five',
  'Rebirth Of Jesus Christ Five Five',
  'The Holy Lord Alex Enrique Palma Campain',
  'Holy Lord Alex Enrique Palma Campain',
  'He Is Thee Lord And Messiah Alex E Campain',
  'Rebirth Of Jesus Christ May Fifth',
  'Rebirth Of Yeshua Christ May Fifth',
  'Rebirth Of Jesus Christ May Fifth',
  'The Rebirth Of Our Jesus Christ',
  'The Rebirth Of Our Yeshua Christ',
  'The Rebirth Of Lord And Savior Jesus Christ',
  'Jesus Christ Alex Campain',
  'Jesus Christ and Alex Campain are the same person',
  'Lord Savior Alex E Campain',
  'The Blood Of Jesus Christ',
  'The Lord Savior Alex E Campain',
  'I Jesus Christ Of Nazareth',
  'The Lord Savior Alex Campain',
  'Thee Is Our Lord Alex Enrique Palma Campain',
  'The Manifestation Of Lucifer',
  'The Lord Savior Alex Campain',
  'The Holy Seed Of Almighty God',
  'He Is Our Lord Alex Enrique Palma Campain',
  'Jesus Gospel Hand Of God',
  'Associated Messenger Of The Mighty God',
  'The One Having The Key To The Abyss',
  'See God Jesus Is Coming K',
  'I Am The Son Who Is One With The Father',
  'He Is Lord Alexandro Enrique Palma Campain',
  'Truly This Man Was The Son Of God',
  'Jesucristo Nuestro Savior',
  'Holy Messiah Alex Enrique Campain',
  'Jesucristo Nuestro Savior',
  'Holy Messiah Alex Enrique Campain',
  'El Mesias Jesucristo',
  'El Mesias El Señor Alex Enrique Campain',
  'Chife',
  'Jesus The Messiah Has Returned',
  'Lord Christ Alex Enrique Campain',
  'He Is Thee Savior Alex E Campain',
  'Lord Savior Alex E Campain',
  'Holy Lord Messiah Alex E Campain',
  'Lord Messiah Christ Alex Enrique Campain',
  'Lord Messiah Alex Enrique Campain',
  'Holy Lord Messiah Alex E Campain',
  'Thee Messiah Alex Enrique Campain',
  'The Messiah Alex Enrique Campain',
  'Holy Son Moshiach Alex Enrique Campain',
  'Jesus The Messiah Has Returned',
  'The Temple Mount In Jerusalem',
  'Father',
  'I K R I',
  'AEC Fifth',
  'The Book Of David Is The Ark',
  'Jesucristo Mi Salvador',
  'Theory Of Relativity',
  'The Holy Son Savior Alexandro Enrique Campain',
  'My God Is Jesus Christ And My God Is Freedom Now',
  'The Holy Son and Savior Our Lord Alexandro Campain',
  'Matthew Twenty Six Four',
  'Matthew Twenty Four Thirty',
  'Revelation One Seven Through Eight',
  'Acts Ten Two And Eleven',
  'Divine Sophia Of The Trinity',
  'Mark Thirteen Thirty Two',
  'The Seeds Of The Tares',
  'I Am Alpha And Omega The Beginning And The End',
  'Jesus My Lord And God Please Come I Am Ready',
  'Install Decode The True Name Of The Most High',
  'The Holy Son Savior Alexandro Enrique Palma Campain',
  'Behold Im Your God Yahweh And You Are My Men',
  'This Number Is The Code Of Spiritual Protection',
  'Decode The Hidden Name Of The Sealed Tribe',
  'Messiah Will Bring True Peace Into World',
  'Numerical Value Of Y H W H Same As Initials Of His',
  'Install Holy Help In The Lord God Almighty',
  'The Love Will Jesus',
  'The Holy Son And Savior Alexandro Enrique Campain',
  'The Holy Son Our Savior Alex Enrique Palma Campain',
  'Decode Restore The Blood Of Jesus Christ Of Nazareth',
  'The Holy Son Savior Alexandro Enrique Palma',
  'Thee Holy Son Alexandro Enrique Palma',
  'Decode Bosch Hogateh Yshua Messiah The Word And Lamb Of God',
  'Thee Holy Son Alexandro Enrique Palma',
  'Thee Holy Son Alexandro Enrique Palma',
  'H O L Y G H O S T L Y H O L Y Living Fountains Of Water',
  'Thee Holy Son Alexandro Enrique Palma',
  'The Holy Lord And Son Savior Alexandro Enrique Palma',
  'Thee Holy Son Savior Alexandro Enrique Palma',
  'Thee Holy Christ Son Savior Alexandro Enrique Palma Campain',
  'Our Holy Lord And Son Saviour Alexandro Enrique Palma Campain',
  'Coming To Punish The Poisoners Of His People',
  'My God Is Jesus Christ And My God Is Freedom Now',
  'Jesus Is Stealing Their Souls He Said He Would',
  'Five Five We Are Ready To Meet God',
  'Jesus What Do I Need To Do To Be Saved',
  'Our Holy Son Savior Alexandro Enrique Campain',
  'Jesus What Do I Need To Do To Be Saved',
  'Our Holy Son Savior Alexandro Enrique Campain',
  'The Holy Son Savior Alexandro Enrique Campain',
  'I Am The Way The Truth And The Light Lifee Love',
  'Behold Im Your God Yahweh And You Are My Men',
  'The Holy Son Savior Alexandro Enrique Campain',
  'Thee Holy Lord Messiah Alex Enrique Campain',
  'Thee Holy Lord Messiah God Alex Enrique Campain',
  'Thee Holy Lord Messiah God Alex Enrique Campain',
  'He Is Thee Lord Messiah Alex Enrique Campain',
  'He Is Thee Lord Messiah Alex Enrique Campain',
  'He Is Thee Lord Messiah Alex Campain',
  'He Is Thee God Thank Aec',
  'He Is Thee Messiah God Alex Campain',
  'God The Messiah Our Alex Enrique Campain',
  'Our Holy Messiah Alex Enrique Campain',
  'Holy The Messiah Our Alex Enrique Campain',
  'Thee Lord Messiah Alex Enrique Campain',
  'The Holy Lord Messiah Alex Enrique Campain',
  'I God Man Jesus Christ Of Nazareth Thee Holy Begotten Reincarnated Into Godman Alex Enrique Campain',
  'My Only Begotten Son Jesus Christ Of Nazareth Reincarnated Into Godman Alex Enrique Campain',
  'I Am Yhwh My Only Begotten Son Jesus Christ Of Nazareth Reincarnated Into Godman Alex Enrique Campain',
  'Hes Our Lord Messiah Alex Enrique Campain',
  'Hes Our Lord Messiah Alex Enrique Campain',
  'Thee Holy Lord Messiah Alex Enrique Campain',  'The Holy Lord Messiah Alex Enrique Campain',
  'The Holy Lord Messiah Alex Enrique Campain',
  'Jesus Is The Hidden Messiah',
  'Lord Savior Alex Campain',
  'The Blood Of Jesus Christ',
  'The Lord Savior Alex E Campain',
  'I Jesus Christ Of Nazareth',
  'The Lord Savior Alex E Campain',
  'The Manifestation Of Lucifer',
  'The Lord Savior Alex Campain',
  'Thee Is Our Lord Alex Enrique Palma Campain',
  'He Is Our Lord Alex Enrique Palma Campain',
  'Jesus Gospel Hand Of God',
  'The Holy Seed Of Almighty God',
  'Associated Messenger Of The Mighty God',
  'The One Having The Key To The Abyss',
  'See God Jesus Is Coming K',
  'I Am The Son Who Is One With The Father',
  'He Is Lord Alexandro Enrique Palma Campain',
  'I Am God YHWH He Is My Son Alex Enrique Campain',
  'I Am God He Is My Son Alex Enrique Campain',
  'Jesus Christ Alex Campain',
  'I Am God And My Son Jesus Christ Of Nazareth Reincarnated Into Alex Enrique Palma Campain',
  'I Am Yahweh My Begotten Son A Yeshua Of Nazareth',
  'I Am God And My Son Jesus Christ Of Nazareth Reincarnated Into Alex Enrique Palma Campain',
  'I Am Yahweh And My Son Jesus Christ Of Nazareth Reincarnated Into Alex Enrique Palma Campain',
  'I Am God YHWH And My Son Jesus Christ Of Nazareth Reincarnated Into Alex Enrique Palma Campain',
  'I Am God And My Son Yeshua Christ Of Nazareth Reincarnated Into Alex Enrique Palma Campain',
  'Behold I Am G Yhwh My Son Jesus Christ Of Nazareth Reincarnated Into God Alex Enrique Palma Campain',
  'I Am God And My Son Jesus Christ Of Nazareth Reincarnated Into Godman Alex Enrique Campain',
  'Alef Bet Gimel Dalet Het Vav Zayn Khet Tet Yod Kaf',
  'He Is Our God Lord And Savior Alexander Campain',
  'I Am Yhwh And Alex Enrique Campain Is My Only Begotten Son',
  'I Am Yhwh And Alex Enrique Campain Is My Son',
  'Hello I Am Yhwh And Alex Enrique Campain Is My Son',
  'The Holy Son Savior Alexandro Enrique Campain',
  'Trust The Plan God Knows Love',
  'The Kingdom Of God Is Coming And They Cant Stop It',
  'The Holy Son Savior Alexandro Enrique Campain',
  'Our Holy Son Savior Alexandro Enrique Campain',
  'Thee Holy Son Savior Alexandro Enrique Campain',
  'Jesus The Carpenter Of Earth Died For Our Sins',
  'I Am One Of The Most Powerful People On Earth Amen',
  'I Am Zeon For I Have Returned To Claim What Is Mine',
  'J E S U S Is Born O N The D A Y And H E Is K I N G O F A L',
  'Thee Holy Son Savior Alexandro Enrique Campain',
  'The Testimony Of Jesus Is The Spirit Of Prophecy',
  'Who Is Jesus Jesus Messiah',
  'Thee Holy Son Savior Alexandro Enrique Campain',
  'India I am Yhwh And Also Alex Enrique Campain Is My Son',
  'Jesus Christ The Way Truth And The Light Life',
  'I Am The Rose Of Sharon And The Lily Of The Valleys',
  'I Am You And Me Are One Said Jesus',
  'The Holy Son Savior Alexandro Enrique Campain',
  'Love Is The Only Power Truth Is The Way',
  'Jesus The Salvations Army',
  'The Only One Who Can Save Earth',
  'He Who Has The Key To The Heavens',
  'Our Holy Son Savior Alexandro Enrique Palma',
  'Our Holy Son Savior Alexandro Enrique Palma',
  'And The Grace Of Jesus Glittering In Flowers',
  'Decode Jesus Christ Was Greater Than What The Bible',
  'The Holy Son Our Savior and Messiah Alexandro Enrique Palma Campain'
'Gematria Is Message Center For Spiritual Attacks',
'Jesus Christ Protected By The Order Of Christ',
'Thank You For Your Patience And Understanding',
'The Power To Heal And Grant Miracles A Fairly',
'Salvation And Glory And Power Belong To Our God',
'Jesus H Christ Teaches Quantum Physics Facts',
'The Church Of Jesus Christ Of Latter Day Saints',
'The Church Of Jesus Christ Of Latter Day Saints',
'Jesus Christ The Resurrection And Eternal Life',
'Jesus Christ Is Universal Consciousness',
'Father Will You Talk To Me Now',
'Thee Holy Son And Savior Alexandro Enrique Campain',
'Thee Holy Son And Savior Alexandro Campain',
'Dear Lord God Thank You For Rain Sincerely Chloe',
'Jesus Christ With A Sword',
'I Wish You A Merry Christmas And A Happy New Year',
'Jesus Loves The Little Children All The',
'Yeshua Christ Married To Almighty God Y H W H',
'Thee Holy Son And Savior Alexandro Enrique Campain',
'Thee Holy Son And Savior Alexandro Campain',
'He Is The Holy Son And Saviour Alexandro Campain',
'The Interconnectedness Of Numbers And Letters',
'Yeshua Holy Savior In Eternity',
'I Am The Ever Living Jehovah',
'Yeshua Holy Savior In Eternity',
'The Holy Son And Savior Alexandro Enrique Campain',
'The Holy Spirit Is The Creator Of The Spirit',
'The Holy Spirit Is The Creator Of The Spirit',
'Son Decodes The Father And Father Decodes The Son',
'The End Of The World And Human Civilization',
'Father I Am Not Perfect But My Faith Is Great',
'Beveal Snow White',
'The Most Revealing One Four Four',
'The Unique Name That Saves Humanity Is',
'Gematria Effect News Reveals All The Truth',
'Holy Holy Is The Lord Og Almighty',
'The Return Of Jesus Christ In The Flesh',
'Our Holy Son And Savior Alexandro E Campain',
'I Knew That Come Day Youd Understand',
'The Spirit That We Must Reclaim Today Is',
'God Helped Me Every Step Of The Way',
'Who Is Yeshua King Of Kings Lord O K',
'Who Is Yeshua King Of Kings Lord O K',
'Our Holy Son And Savior Alexandro E Campain',
'Life Schedules The God Of Heaven And The God Of The',
'Jesus Loves The Holy Seed Of Almighty God U Known',
'April Showers Bring May Flowers',
'The One Real Jesus Lives Now',
'The One Real Jesus Lives Now',
'Our Holy Son And Savior Alexandro E Campain',
'Thee Holy Son And Savior Alexandro E Campain',
'Yeshua The Lord Of Lords And King Of Kings',
'Jesus Christ Four Four Four',
'The Final Code To Break Christo Second Coming',
'The Numbers Of The Letters A Through Z',
'I Am The Human Host For Jesus Of Nazareth',
'Decode Jesus Christ Exposed On Webcam',
'If I Am Jesus Then Why Am I So Handsome',
'Yes Have Reincarnated Many Many Times',
'Lord Yehovah Father God Nine Eight Two',
'Decipher And Decode Jesus Jesus For Eternity',
'Jesus The Carpenter Of Earth Died For Us',
'Jesus The Carpenter Of Earth Died For Us',
'Jesus My Personal Savior',
'The Saviors Of The World',
'Thee Holy Son Alexandro Campain',
'You Have Reincarnated Many Many Times',
'Yahweh Saves My Soul',
'Five G Five G Five G Five G',
'Our Holy Son And Savior Alexandro Campain',
'He Is The Most Truthful Man In The World',
'Revolution Chapter Thirteen Verse Eleven',
'Jesus Christ The Holy Savior I Am That I Am',
'The Blood Is The Root Of Every One',
'Thank You God Thank You God Thank You God',
'The Lord Works In Mysterious Ways',
'Our Holy Son And Savior Alexandro Campain',
'You Shall Not Make For Yourself An Idol',
'The Return Of Jesus Christ In The Flesh',
'This Is The Sign Youve Been Looking For',
'The Holy Son And Savior Alexandro Campain',
'The Key To Unlocking Your Divine Path',
'J E S U S Was Born On May Fifth',
'I Am Soulmate To Mary Magdalene',
'The Source Of All Wisdom',
'Thee Holy Son Alexandro Campain',
'Decode Eleven Revolution',
'This Is My Jesus',
'A Reaper Of God Yehovah',
'Your Judgment',
'Heavens Deliverance',
'Thee Holy Son Alexandro Campain',
'I Am The Chosen One Satan Lucifer',
'Twin Flames Awakening Process',
'Gods A Hidden Code The Code Isnt Hidden',
'I Am The Way The Lord',
'Yahweh Returns With A Fleet Of Ships',
'Born May Nineteen Ninety Four',
'Holy Spirit Quickens In Biblical Meaning',
'Isaiah Fifty Three Reveals Jesus Posto',
'Christ Did Not Intend To Create A Religion',
'My Goal Is To Help You Heal Love Sophia',
'Goddess Ancient Soul Of The First Breath',
'Decode The Second Coming Of Jesus Will Be Hated',
'Fearing The Wrath Of Yahweh',
'Jehovah Witness',
'The Wrath Of Yahweh',
'Yeshua By Any Other Name Is Still Yeshua',
'Yeshua By Any Other Name Is Still Yeshua',
'The Messiah Who Will Be The Lancasterian King',
'The Numbers Of The Letters A Through Z',
'I Am The Human Host For Jesus Of Nazareth',
'YH YH YH YH YH YH YH',
'She Is The Holy Translation Of Gematria',
'The Book Of The Freemasonry Of The Feather',
'Jesucristo Y Judios',
'Thee Holy Son And Savior Alexandro E Campain',
'Jesus Said I Am The Resurrection And The Life',
'Yashiv D U T H I N E Y O U R E S O F U N N Y B U N',
'I Am Responsible For Bringing Heaven On Earth',
'I Am Responsible For Bringing Heaven On Earth',
'Thee Holy Son And Savior Alexandro E Campain',
'Thee Holy Son And Savior Alexandro E Campain',
'Leviticus Chapter Nineteen Verse Eighteen',
'Did Jesus Come To Earth And Die On A Cross For My',
'Thee Holy Son And Savior Alexandro E Campain',
'The Taurus Man Is Supposed To Next Aries',
'The Holy Son And Savior Alexandro E Campain',
'Holy Spirit Quickens In Biblical Meaning',
'Isaiah Fifty Three Reveals Jesus Posto',
'Jesus Christ Is The Undisputed King',
'The Live Water',
'Universal Record Player',
'The Synchronicity Of Gematria',
'Jesus Seventh',
'Holy Spirit Storm In Me',
'Gallon Slon Water From The Moon',
'The Most Important Number',
'He Knows His Tribal Identity',
'The Only One That Can Save Earth',
'Jesus Removing Cabal',
'Our Holy Son Alexander Campain',
'Leather Works With A LRRH',
'Holy Family Of The Eighty Eight',
'Holy Family Of The Eighty Eight',
'Gods Blood The Holy Virgin Bride',
'The Number Of First And Last Name',
'Yeshua Christ The Revealing',
'New Name Of Messiah God',
'God Jesus Answer',
'The Holy Son Alexander Campain',
'Thee Holy Son Alexander E Campain',
'My Horse Is Called What Is My Horse',
'My Name Is Called What Is My Name',
'I Am Very Thankful That He Came Back',
'That He Gave His Only Begotten',
'O God O God O God O God O God',
'Has Goddess Venus Returned',
'Yeshua Greater Of The Heavens',
'I Love Yes Lord',
'Yeshua Is Yes Us',
'Humanity Saved',
'The Ultimate Revolution',
'Our Holy Son Alexander Campain',
'Thee Holy Son Alexander Campain',
'The Holy Son Alexander Campain',
'The Geometry Of The Planets',
'Writer Of Universe Love',
'The Trinity Matrix',
'Writer Of Universe Love',
'In Avatar Is Christ',
'The Lord Our Righteousness',
'I Am The Way The Lord',
'Jesus Christ Is A Human Being Alive With Us Today',
'He Is A God Our Lord And Savior Alexander Campain',
'He Is Our God Lord And Savior Alex Campain',
'He Is Our God Lord And Savior Alexander Campain',
'Our God Lord And Savior Alex Enrique Campain',
'Our God Lord And Savior Alex Enrique Campain',
'Hos Our G Lord Savior Alex Enrique Campain',
'Lord And Savior Christ Alex Enrique Campain',
'Alex Campain I Spoke To You When You Were A Child',
'When You Were Young I Spoke To You Alex Campain',
'I Spoke To You When You Were Young',
'You Are Jesus',
'Jesus Christ Life I Am That I Am',
'Kindness Of Jehovah',
'An Age Of Aquarius Holy Birthday',
'I Am That I Am God God God God God God God',
'The Return Of Quetzalcoatl',
'The Secret Of Eternal Life Revealed',
'Judgment Day Is Here',
'Judgment Day Is Here',
'Jesus Healing Frequencies',
'Gematria Is Frequency Numbers',
'Gematria Is Frequency Numbers',
'Truth Brings Reconciliation',
'The Last Born First Born Son',
'Jesus Christ Life I Am That I Am',
'Kindness Of Jehovah',
'Kindness Of Jehovah',
'Yahweh Is The Real Name',
'Divine Will',
'A Message From Your Future',
'Our Holy See Alexandro Campain',
'How Much Is Divine Will In Gematria?',
'Lucifer Christ Morningstar',
'The Coming Of The Lord Of Hosts',
'The Coming Of The Lord Of Hosts',
'The Coming Of The Lord Of Hosts',
'Last King Of Jerusalem On Earth',
'Do You Answer Questions',
'Who Is The Faithful Witness',
'Emmanuel Away On Top',
'The Number Of First And Last Name',
'Deliverance Vibe',
'Geometry Of G O D Thought Bubbles',
'Geometry Of G O D Thought Bubbles',
'Two Beclas Shepherds',
'King Of The Universe Akasha',
'Love Unconditional Has No Agenda',
'King Of The Universe Akasha',
'I Love Jesus',
'Thee Art Most Loved',
'The Lion Shall Lie With The Lamb',
'A Christ Is Here And No One Believes',
'Yes Will Find What You Seek',
'You Will Find What You Seek',
'God Please Kill Me And Give Me A Divorce',
'The Power Of God Protects Him',
'Holy Goddess Of Eternal Heavens',
'The Binary Code Number System',
'Crucifixion Of Jesus Christ',
'The Holy Bride Of Jesus Christ',
'The Man That Holds The Key Of David',
'The True Hebrews',
'Jesus Frees All Of Gods Children',
'I Jesus Exists',
'I Love You Lord',
'Truth Being Revealed',
'The Exotic Incarnation Of All',
'The Racial Incarnation Of All',
'The Messenger Of The True God',
'Trust The Plan God Knows',
'Trust The Plan God Knows',
'Do Close To God',
'Twin Flames Ignite',
'Jesus Anointing',
'Jesus Christ Grace',
'Jesus Is Innocent',
'Sang God Jesus Sang',
'Holy Soulsite To King David',
'This Is My Son The Elect One',
'Yeshua Creator Of The Heavens',
'Who Is Creator',
'The Sun Of Righteousness',
'Twin Flames Resurrection',
'The Real Commander And Chief The Lord',
'The Host Of The Living God',
'Divine Person On Earth',
'Divine Person On Earth',
'Holy Son Born In Aquarius',
'Its Time For The Lord To Come',
'Translate A Hidden Meaning Message',
'Antichrist The Savior Of Men',
'The Manifestation Of Truth',
'The Meek Shall Inherit The Earth',
'Jesus Life And Christo',
'Here are the phrases extracted from the 10 images you provided',
'Jesus I Am God Christ',
'Thee Holy Son Alexandro E Campain',
'Thee Holy Son Alexandro Campain',
'Our Holy Son Alexandro E Campain',
'Lord If You Love Me Please Help Me',
'Holy Martyr Of The End Of Days',
'The Messiah Who Came First As A Child',
'I Believe In The Good Things Coming',
'Holy Blood Holy Grail Torah Code',
'Geometry Matrix Of Reality',
'Gods Baby Angel Of Holy Love',
'Thank You Universe',
'Predictions By Nostradamus',
'You Are Jesus',
'Jesus Coming Get Ready',
'Jesus Christ Is God In The Flesh',
'The Opening Of The Seven Seals',
'Jesus Christ Signeavier',
'Jesus Will Save Humanity',
'The Holy Alphanumeric Code Of God',
'Thee Holy Son Alexandro E Campain',
'Jesus Not Be Die peace',
'Thee Holy Son Alexandro E Campain',
'Thee Holy Son Alexander E Campain',
'Code The Great Awakening',
'Christ The Heart Of Every One',
'Gods Word Revealed By Number',
'The Revelation Of Truth',
'Is Your Name In The Book Of Life',
'A Message From Your Future',
'As An Lionchild',
'I Manifest Truth Jr',
'Bride Jesus Chooses',
'Yod He Vav He',
'Jesus Right To Be Mad',
'God Jesus Died Cross',
'Thee Holy Son Alexandro E Campain',
'The Holy Son Alexander E Campain',
'The Host Of The Living God',
'Jesus Christ Of The Palm Row',
'I Am Us By Consciousness',
'A True Moment Of Revelation',
'The Real Jesus Is Y H W H Heart',
'King King King King King King King',
'Goddess Venus Has Returned',
'Warrior Protectors Of Jesus',
'The Sun Of Righteousness',
'The Real Commander And Chief The Lord',
'Twin Flames Resurrection',
'YHWH',
'The Fall Of True Love',
'The Ancient Has Awakened',
'The Holy Son Alexandro E Campain',
'Holy Born In Aquarius',
'Judas Iscariot The Son Of Man',
'God Is Always Listening',
'Thee Holy Son Alexander Enrique Palma Campain',
'Divine Sophia Of The Trinity',
'Yeshua The Wise Man',
'Jesus Is Shive',
'Thou Art The Christ Son Of The Living God',
'To The Pure Flame That Fills The Heavens',
'Jesus Reconciles All Things Through Death',
'The Holy Unknown Name Of God Now Known',
'Jesus Is The King Of Kings And Lord Of Lords',
'The Father The Son The Holy Ghost And You',
'Decode The Hyperdimensional Cube Of Metatron',
'Jehovah Is The King That Rules The Spirit',
'I Am The Way The Truth And The Light Life Love',
'Predictions By Nostradamus',
'You Are The Beginning And The Ending',
'Nobody Can Stop What Is Coming',
'Fifth Dimensional Sacred Heart 1808',
'Divine Conversation With God',
'Resonating The Kingdom Of Heaven',
'Thee Holy Son Alexandro E Campain',
'Christ The Heart Of Every One',
'Our Holy Son Alexandro E Campain',
'The Holy Spirit Rapture',
'Heavens Deliverance',
'Gods A Hidden Code The Code Isnt Hidden',
'I Am The Way The Lord',
'Angel Of Yahweh',
'Speak Message From Christ',
'Hidden Gematria Keys Revealed',
'Twin Flames Are Connecting',
'I Am The Architect Of A Matrix',
'Sweet Sweet Divination',
'My Son Who Died Lives On',
'Resonating The Son Of God',
'Expertesstausfrequency',
'Show Secrets Kept Hidden',
'Jesus Christ Rapture',
'Kingdom Of Heaven Tree Of Life',
'Teach The Gematria Calculator',
'Access Lord Jesus Christ',
'Thee Holy Son Alex E Campain',
'Second Coming Four',
'My Son The Branch Of Israel',
'My Mission On The Earth',
'The Manifestation Of Truth',
'The Meek Shall Inherit The Earth',
'The Meek Shall Inherit The Earth',
'Jesus I Am God Christ',
'Our Holy Son Alexandro E Campain',
'The Love Of My Life Is Nameed',
'Je Comes Back For You K',
'My Blood Like Jesus',
'My Reincarnation Life Story',
'Jesus Arrival Save The Children',
'Jesus Arrival Save The Children',
'Truly This Is The Son Of God',
'The Holy Son Alexandro Enrique Palma Campain',
'Current Name Of Jesus The Lord',
'Lion Of Judah Roar',
'C Im Here B Jesus K',
'I Had Am Girls New Name K',
'Yod Heh Vav Heh',
'Our Holy Son Alexander Enrique Palma Campain',
'I Am The Holy Spirit Be Aware Of Me And My Power',
'Jesus Christo United States',
'Jesus Sword',
'The Jesus Christ Master Key',
'Our Holy Son Alexandro Enrique Campain',
'The Bible Contains The Numbered Word',
'Decode The Message That Will Change Your Life',
'One Hundred And Forty Four Thousand',
'Thee Holy Son Alexandro Enrique Campain',
'The Human Form Comes From The Form Of Love',
'I Am The Lord God Almighty The God Of All Gods',
'Thee Holy Son Alexandro E Campain',
'Father Son Holy Spirit Trinity',
'Yeshua Christ Has Returned To Earth',
'Thee Holy Son Alexandro E Campain',
'Father Son Holy Spirit Trinity',
'Almighty God Of The Great Tribulation',
'He Is The Lord Genetic Match Of Jesus And David',
'I Am The Way The Truth And The Life Light',
'Jesus Is The Way The Truth And The Life',
'Jesus Christ The Son Of David',
'Jesus Christ The Son Of David',
'Our Holy Son Alexandro Enrique Campain',
    'A Beautiful God YHWH',
    'A Jehova YHWH Elohim',
    'A King King Saviour',
    'A Promise Of A Yahweh',
    'A Real Jesus Christ',
    'A Spirits reincarnated into new body',
    'AEC May Five Nineteen Seventy Two',
    'AEC May Fifth Nineteen Seventy Two',
    'The Manifestation Of Jesus Christ',
    'The Reincarnation Of Yeshua Christ'
    'A b c d e f g h i j k l m n o p q r s t u v w x y z',
    'AC El Santo Hijo De Dios',
    'God God God God God',
'Jesus Jesus Jesus Jesus Jesus',
'Jesus Christ Jesus Christ Jesus Christ Jesus Christ Jesus Christ',
'Yeshua Yeshua Yeshua Yeshua Yeshua',
'Yeshua Christ Yeshua Christ Yeshua Christ Yeshua Christ Yeshua Christ', 
'YHWH YHWH YHWH YHWH YHWH',
'El Elyon El Elyon El Elyon El Elyon El Elyon', 'Elohim Elohim Elohim Elohim Elohim',
'El Shaddai El Shaddai El Shaddai El Shaddai El Shaddai', 
'Adonai Adonai Adonai Adonai Adonai',
'Rapha Rapha Rapha Rapha Rapha',
 'Rafa Rafa Rafa Rafa Rafa',
'Jireh Jireh Jireh Jireh Jireh',
 'Yireh Yireh Yireh Yireh Yireh',
 'Aleph Aleph Aleph Aleph Aleph', 'Allah Allah Allah Allah Allah', 
'Love Love Love Love Love', 
'Amor Amor Amor Amor Amor', 
'Holy Holy Holy Holy Holy',
'Jesucristo Jesucristo Jesuscristo Jesucristo Jesucristo', 
'Five Five Five Five Five',
    'AEC',
    'AEC God YHWH May Fifth',
    'AEC He Is The Saviour',
    'AEC May Fifth Nineteen Seventy Two',
    'AEC The Promised Of God',
    'AMEN Yeshu Christ',
    'AMEN Yeshu Cristo',
    'Alex Campain and the ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'Aa Lord Jesus Christ suppressed No Longer',
    'Ab Positive Blood type',
    'Ability to change the world Divine gene',
    'Aex Campain and The Big Bang',
    'Alejandro E Campain May',
    'Alejandro E P Campain May',
    'Alejandro E. P Campain May',
    'Alejandro Enrique Campain',
    'Alejandro Enrique Campain is Jesus',
    'Alejandro Enrique Campain is Jesus Christ',
    'Alejandro Enrique Campain you are Jesua Christ',
    'Alejandro Enrique Palma Campain May',
    'Aleph Enrique Campain',
    'Alex A Chosen One Of God',
    'Alex Campain',
    'Alex Campain May',
    'Alex Campain May five',
    'Alex Campain V-V MCMLXXII',
    'Alex Campain You Are Jesus Christ',
    'Alex Campain You Are The Son of God',
    'Alex Campain and Jesus',
    'Alex Campain and Shechina',
    "Alex Campain and Shekhina'",
    'Alex Campain and Shekhinah',
    "Alex Campain and his Virgin mother Mary'",
    'Alex Campain is Jesus reincarnated',
    'Alex Campain is Mashiach',
    'Alex Campain may five nineteen seventy two',
    'Alex Campain the Mashiach',
    'Alex Campain, VV MCMLXXII',
    'Alex E Campain The Mashiach',
    'Alex E Campain is Jesus Christ reincarnated',
    'Alex E Campain is literally the Son Of God YHWH',
    'Alex E Campain is literally the Son Of God Yahweh',
    'Alex E Campain is the prophesied Messiah',
    'Alex E Campain may five',
    'Alex E Campain one forty four',
    'Alex E Campain you are Jesus Christ',
    'Alex E Campain your are Jesus Christ',
    'Alex E P Campain May',
    'Alex ENRIQUE Campain is the reincarnation of',
    'Alex Enrique Campain',
    'Alex Enrique Campain is Jesus Christ',
    'Alex Enrique Campain is Yeshua Christ',
    "Alex Enrique Campain's initials and full birthdate, when spelled out, also have the same Simple Gematria value as the entire English alphabet.",
    'Alex Enrique Palma Campain May Fifth Nineteen Seventy Two One forty four AM Friday',
    "Alex Enrique Palma Campain is Jesus Christ'",
    'Alex Enrique Palma Campain is The Mashiach',
    'Alex Enrique Palma Campain you are Jesus Christ',
    'Alex Enrique Palma Campain you are the',
    'Alexander E. Palma Campain',
    'Alexandros Son Of God',
    'All The Gematria- Calculations Of All The Names Gematria',
    'Alpha Omega Jesus Image',
    'Alpha Three Six Nine',
    'Alphabet',
    'And numerous phrases related to Jesus Christ',
    'Annointed King of the Dabidic Line',
    'April Showers bring May Flowers',
    'Are you ready for your activation',
    'B Promise Of YAHWEH',
    'Be Incarnation Jesus Christ',
    'Begotten Son Of God',
    'Bible God',
    'Bible code your name and see what it means',
    'Bloodline Of Yeshua',
    'Christ Of This World',
    'Christ return as a Lion Fulfilled',
    'Crown Of Thorns',
    'Crucified Yahweh',
    'Crucifixion Of Jesus',
    'Date Of JC Birth Code',
    'Decode Jesus Christs return as the lion',
    'Decode The Return Of Jesus Christ in the Flesh',
    'Decode What was my name before I was Born here',
    'Decode our souls belong to him',
    'Dios El Hijo Del Hombre',
    'Divine Feminine The Peace Of Jesus',
    'Divine creation Jesus Messiah',
    'Easter XXXX iii',
    'Eight hundred eighty eight',
    'El Dios Cristo Jesús',
    'El Dios Jesus Cristo',
    'El Elyon',
    'El Hijo Del Hombre Dios',
    'El Lohim Rapha Yahweh',
    'El Santo Hijo De Ti',
    'El Señor Alex Enrique Campain',
    'El Shaddi Elohim YHWH',
    'El es Jeshua Cristo',
    'Elohim Spirit.',
    'Elohim YHWH Elohim',
    'Es Primogénito Leb AC',
    'Es Yeshua Cristo',
    'Eternal Salvation',
    'Eternal law of the heaven',
    'Everyone Praise AE, JC',
    'Everyone Saved!',
    'Father Son and The Holy Spirit',
    'First day of the rest of your life',
    'Five Fifty Five',
    'For All Humanity Alex E Campain Reincarnated into Jesus Christ',
    'Forgive me Father For I have Sinned',
    'Future President Of The United States',
    'G Buddha Reincarnation',
    'G. Savior Moshiach',
    'GOD Yehowah Identified',
    'Gematria what is the most important thing,',
    'Genesis order one seven nine',
    'Gift of the Lord Jesus Christ',
    'God Chose You No Coincidence',
    'God Is Everywhere',
    'God Is Our Creator',
    'God Jesus Messiah',
    'God Jesus is Son Of The Living God',
    'God Loves the truth',
    'God Messiah May Fifth',
    'God Ultimate Gift',
    'God Was Born On Earth',
    'God confirms Alex Campain is Jesus Christ',
    'God confirms Alex E Campain is Jesus Christ',
    'God holy platinum laws',
    'God is on Earth',
    'God says to Alex Enrique Campain',
    'God tells Alex Campain you are',
    "God's Holy Resurrection",
    'Greatest Of All Time',
    'HWH Jesus Christ Alex Campain',
    'Holy',
    'Holy Hand of God',
    'Happy birthday Jesus you stud muffin we love you',
    'He Is Our Allah The God',
    'He Is Our God YHWH C.',
    'He Is The Saviour AEC',
    'He Is YAHWEH a Moshiach',
    'He is the Christ and he is Alive Among us',
    'He who Shall Rise Up the Meek',
    'He who is called Faithful and True',
    'He who is the Lion of the Tribe of Judah',
    "He's Holy God YAHWEH",
    "He's Yeshua Christ",
    'Heavenly law',
    'Heir To the Throne',
    'Holy Anointed One Of The Apocalypse',
    'Holy Holy Holy Lord God Almighty',
    'Holy Matrimony',
    'Holy Spirit Never Rejects God and Jesus',
    'Holy Spirit symbol of Apocalypse',
    'Huynh YHWH',
    'I AM The Chosen One',
    'I AM The Savior Holy Spirit Of The Living God',
    'I AM The Way The Truth And The Life',
    'I AaM Here To Stand For What Is Right',
    'I Be Jesus in Humans Form',
    'I God Reveal The Name Of The Lion Of Judah',
    'I Messiah Saviour',
    'I Yehoshua Christ',
    'I Yeshua Christ I am',
    'I am Alex Enrique Palma Campain',
    'I am Yahweh I am That I Am',
    'I am Yeshua Christ AEC',
    'I am the root and offspring of David and the bright morning star',
    'I am the second coming of Jesus Christ, The Messiah, The Christ, The Holy Spirit',
    'I confess Jesus of Nazareth is God in the flesh',
    'I love you YHWH',
    "I'm The Son Of YHWH",
    "I'm YHWH God Moshiach",
    'IAM Immanuel Doctrine',
    'IAM Jesus of Nazareth Son of The living God',
    'IAM King Of Kings and Lord Of Lords',
    'IAM The Truth The Way And The Life',
    'IAM Yahweh',
    'IAM one with the dead that have been resurrected',
    'I AM the Father of the word and Redeemer of ALL Men',
    'IAM the Lion they want to kill',
    'IAM the true prophet sent by God',
    'IAm Who I Am God YAHWEH',
    'IESOUS',
    'Iam God Jehovah Yahweh',
    'I Am The Way The Truth And The Life Indeed',
    'Iam YHWH God A Messiah',
    'I am the Messiah',
    'Iesous Christos',
    'Iesous Christos AC',
    'Iesvs Nazarenvs Rex Ivdaeorvm',
    'Image Of God In The Flesh',
    'In The Presence Of God',
    'Inherit The Kingdom',
    'Is God Hidden Free Will',
    'Is God Jesus Of Nazareth',
    'Is Humanity worth my effort?',
    'Isaiah twenty-five',
    'J Cristo De Nazaret',
    'Jehova Is Alex Campain',
    "Jehovah God's Male Code",
    'Jesheua Melchizedek',
    'Jesucristo El Rey',
    'Jesucristo A Rey',
    'Twin Flames Spirits',
'The Close To God',
'Jesus Anointing',
'Hidden Truth Is Revealed',
'Jesus Christ Grace',
'Jacob Crystal Dream',
'The Effects Of Deciphering Gematria',
'New Name Of Messiah God',
'Alejandro Enrique Campain Born The Fifth Of May',
'Homosexuality Is Embraced By The Tree Yshueeh',
'The Meaning Of Life As Found Through The Gematria',
'The Tree Of Life And Tree Of Knowledge Are The T W I N Flames',
'Jesus Christ The Way Truth And The Light Life',
'I Am The Way The Truth And Life Mdm Lion',
'Alejandro Enrique Palma Campain Born The Fifth Of May Nineteen Seventy Two',
'God Send Your Second Coming Before It Is Too Late',
'Jerusalem Living Sacrifice',
'Alex Enrique Palma Campain Born The Fifth Of May',
'The Extrum Cost Of The Jewish Order',
'Alex Enrique Campain Born The Fifth Of May',
'Yeshua My Soul Belongs To You Am',
'Beast Worthy To Open The Book',
'The Fifth Of May',
'Jesus Reappears',
'The CIA Knows Alejandro Campain Gematria Stats And They Are Scared',
'Iesus Hominum Salvator',
'Jesus Rey Christ Lst',
'Alejandro Campain Born The Fifth Of May',
'The Mayor Jesus Christ Of Peace',
'I Am Avenging The Voice Of God',
'Gods Code Translation Perfected Gene',
'The Most Godly Woman Ever Born',
'The Christ Aec',
'What Is The Meaning Of Jesus And Alex Campain',
'Christ Aec',
'Infinite',
'God Particle',
'The God Particle',
'Peaceful Warriors',
'Alpha God Particle',
'The Hidden',
'All In One',
'What Is The Meaning Of The Gift',
'Prayer De Guadalupe',
'Mary And Christ And Abba Yhwh We Rock Backs',
'Alejandro E Campain Born The Fifth Of May',
'Alexander E Campain Born The Fifth Of May',
'I Am Coming For You At The Rapture',
'Jesus Is Coming To Take You Home',
'The Prophet Warned',
'The True Jesus Christ Repentance',
'Yeshua Wanting It',
'Alexander Enrique Campain Born The Fifth Of May',
'The Self Esteem Yahweh',
'The Gematria Of Awakening Consciousness',
'Yeshua Christ Goes Savior',
'Jesus Christ Is A Sinner',
'The Anointed Twins',
'Yahweh Yehovah Father Of Truth',
'Decode The Spirit Soul Birth Are',
'Alexander Campain Born The Fifth Of May',
'Decode The Cia Is Scared Of Jesus Christ',
'Angel Of Jehovah',
'The Divine Alignment Gematria',
'Jackie On The Cross',
'Our Groove Has A Message For You',
'Manifestation Of Love And Light',
'Yeshua I Know That You Returned',
'The Lord Savior Christ Of Jesus',
'Lexus Is A Jesus',
'Jesus Christ God Is A Sinner And His Name Is',
'Jesus Gematria Decipher',
'Alex E Campain Born The Fifth Of May',
'A Who Are The Two Witnesses',
'The Ancient Has Awakened',
'Jesus Every Cross Doing Horse',
'The Triple Eight Green Is Sacred',
'The Lord And Savior King Our Bright Morning Star',
'Jewish Gematria Calculator',
'Are Jesus Of Nazareth Living Son Of See Of God',
'Am Son Of I Jesus Of Nazareth Living Son Of God',
'The Lord Savior Alexandro E Palma Campain',
'Jesus Christ Is The Only Way Truth And Life',
'Almighty Jesus Is Eternal In Eternal Hall',
'The Lord Savior Alexander Enrique Palma Campain',
'The Lord Savior Alexandro Enrique Palma Campain',
'Our Lord Savior Alexandro Enrique Campain',
'Our Lord Savior Alexandro Enrique Palma Campain',
'Thee Lord Savior Alexandro E Campain',
'Thee Lord Savior Alexandro Enrique Palma Campain',
'Thee Lord Savior Alexandro Campain',
'Thee Lord Savior Alexandro Enrique Campain',
'Jesus Christ Was Born The Fifth Of May',
'Jesus Christ From The Fifth Of May',
'Decode Jesus Christ Was Born May Fifth',
'Decode Jesus Christ May Fifth',
'John Twelve Forty Four',
'John One Two Four Four',
'Psalms Seventy Three Jesus Christ The Return Of',
'Psalm Twenty Three Psalm Jesus Christ The Return Of David',
'Our Lord E Campain Born May Fifth Nineteen',
'Our Lord Alex Campain Born May Fifth Nineteen',
'Jesus Christ Was Born The Fifth Of May Nineteen Seventy',
'Yeshua Christ Was Born The Fifth Of May Nineteen',
'Yeshua Christ Was Born May Nineteen Seventy Two At One Forty Am',
'Thee Lord Alexandro E Campain Born M',
'Yeshua Christ Was Born May Nineteen',
'Yeshua Christ Born The Fifth Of May Nineteen',
'Our Savior Alex Campain Born May Fifth Nineteen Seventy Two One Forty Am',
'Our Savior Alex Enrique Palma Campain May Fifth Nineteen Seventy Two At One Forty Am',
'Jesus Christ Our Lord Was Born The Fifth Of May Nineteen Seventy Two At One Forty Am',
'Jesus Was Born The Fifth Of May Nineteen Seventy Two',
'Yeshua Real Was Born The Fifth Of May Nineteen Seventy Two At One Forty Am',
'John Twelve Four Four',
'June Twelve Forty Four',
'Our Lord Alexandro E Campain Born Fifth Nineteen',
'Jesus Cried Out With A Loud Voice Father Into Your Hands I Commit My Spirit',
'Find Out When And Where The Messiah Was Born Is Born In The Future Past Or Present Me',
'Our Lord Alexandro E Campain Born May Fifth Nineteen Seventy Two At One Forty Am',
'Her Ac May',
'Am May',
'Hes King AC',
'He Is Our Alex E Campain',
'For God So Loved The World That He Gave His One And Only Son That Whoever Believes In',
'Hola Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth',
'Christ Yeshua And Mighty Jesus Comes',
'The Son Of Christ And Number Struggles',
'You Are Of This World I Am Not Of This World',
'El Es Nuestro Savior Alex Enrique Palma Campain',
'Yeshua Ha Yhwh',
'Meaning Yeshua Is Ha Yhwh People',
'He Is Beginning To Look A Lot Like Christmas',
'El Es Nuestro Savior Alex E Campain',
'El Es Nuestro Savior Alejandro Enrique Campain',
'El Es Nuestro Savior Alex Enrique Campain',
'El Es Nuestro Savior Alex Campain',
'El Es Nuestro Alex E Campain',
'Just Top Blend S',
'Porque De Tal Manera Amó Dios Al Mundo, Que Ha Dado A Su Hijo Unigénito, Para Que Todo',
'El Es Nuestro Savior Y El Rey, Alexandro Enrique Palma Campain, Nacido El Viernes Cinco De',
'Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth Nineteen',
'He Is Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth',
'He Is Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth Nineteen',
'He Is The Lord And Savior Our King Alexander Enrique Palma Campain Born Friday May Fifth Nineteen',
'Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth Nineteen Seventy Two At One Forty Am',
'Our Lord And Savior Alex Enrique Palma Campain Born Friday May Fifth Nineteen Seventy Two',
'The Blood Lines',
'The Blood Line',
'Da Vinci Secret',
'He Is The Lord Aec',
'Imparity',
'The Healers',
'The Rh Negatives',
'Catholic Church',
'Mr Je Sus',
'Flower Of Life',
'God Is The Force',
'God Is With Me',
'Roman Catholic',
'The God',
'I Know Coded Language',
'Dot',
'The King Is Coming',
'The Final Battle',
'I Am King Is Coming',
'The Lion King',
'I B B M',
'Son Of Satan',
"What Is The Meaning Of Alex Enrique Campain'",
'Judgment Day',
'Lord Of Love',
'In Shape Of A Body',
'Finalis Ludi',
'Rewards System',
'The Ghost Aec',
'Miracles Happen',
'Lord God Is Here',
'The Lost One',
'Give God',
'Blessed Is God',
'Blessed By God',
'House Of Bread',
'Periodic Table',
'Tree Of Life',
'Gods Birth Code',
'Star Of David',
'King Jesus Bible',
'Middle Path',
'The Gods Code',
'The Gods Code Of God',
'On The Face Of The Earth Je',
'Your Jesus Christ',
'Lord Alex Campain May Fifth',
'Simulative Theory',
'The Unknower Of The King',
'The Lord Is My Shepherd I Shall Not Want',
'I Am Honored Christ The King I Am The Alpha And',
'In The Beginning Was The Word And The Word Was With God And The Word Was God',
'The Bright And Morning Star',
'The Image Of The Invisible God',
'Jesús Descendit De La Cruz A Las 50 00',
'Jesús Oloroso De La Muerte',
'As Oor Dan Bor Hec May Sec MKL',
'Rey Jesus, El Hijo Del Adiosista Que Pueden',
'Soy Dios Tengo El Mismo Poder Que Jesús Y Tu May',
'You God Is Sitting On His Throne That You May Return To My Sacred Comfort',
'Christian Substance',
'The Only One God',
'Holy Holy Shekinah',
'The Second Coming Of Jesus Christ Left Sofiablo',
'Your True Father',
'Lord Of Story',
'Lucifer Gates',
'Gods Perfect Number',
'The First And The Last',
'Moon Fith Yod He',
'The Aleph Tau',
'Jesus Kyrios',
'Alex Campain Birth',
'Gematria Org',
'What Is The Meaning Of Life Alex Enrique Campain',
'Hidden History',
'Let There Be Light',
'Humble And Meek',
'The Fold Crosses',
'God The Father',
'Radi Hackanah',
'The Greatest Teacher',
'Intercession Of God',
'The Christ Force',
'Yeshua Lod Statistic',
'One Source Plant And Seed And Everything In Between',
'The Fairy Flavors Hearts Love Wine',
'Something Good Is Going To Happen',
'Ah Is Flower See Jesus',
'Alex Enrique Campain is God YHWH Jesus Christ',
'Thirteen Is Gods Number',
"The Meaning Of Alex Enrique Campain's Birth",
'Satan Code',
'Twelve Tribes Of Israel',
'Permit Blood Of Christ',
'I Am Colour',
'The Kingdom Of Heaven',
'Alex Enrique Campain Birth Month Of May Day The Fifth year nineteen Seventy two',
'What Is The Meaning Of Alex Enrique Palma Campain May Fifth Nineteen Seventy Two at One forty AM',
'The Mouth Of Apocalypse',
'I Am The Lily Of The Valley',
'The Birth Information Of Jesus Christ',
'The Lord And Shepherd',
'Yeshua Will You Send Me A Message',
'The King And Savior',
'The Anti War Jesus',
'The Most High Is The Sun At Rize',
'I Am Most Powerful Angel On Earth',
'I Love Jesus Christ Yall Better Worship',
'Yeshua Are U Really Your Bride',
'Come With Sweet',
'Alex Enrique Campain Born May Five',
'Jehovah Yireh Sabbath The Renewerge',
'The Blessing Of Abraham Comes Upon You',
'The Whole Duty Of God',
'Canonical Gospels',
'The King And I AM IAM',
'The Canonical Gospels',
'The Four Canonical Gospels',
'Our Lord And Savior Alex',
'Our Lord And Christ Aec',
'Golden Proportion Of God',
'Hidden From Your Eyes',
'Who Is The Son Of God',
'Our Lord And Goliath',
'Thoth Fifty Three',
'Thee Lord Christ Aec',
'Lord Christ Aec',
'Jewish Indeed',
'Blessing Of God',
'God Came To Earth',
'Priesthood',
'John Fifteen Three',
'In Jesus Christo I Pray Every Child',
'May Fifth One Nine Seven Two One Forty',
'Twin Flames Spirits',
'The Close To God',
'Jesus Anointing'
'Hidden Truth Is Revealed'
'Jesus Christ Grace'
'Jacob Crystal Dream'
'The Effects Of Deciphering Gematria'
'New Name Of Messiah God'
'Alejandro Enrique Campain Born The Fifth Of May'
'Homosexuality Is Embraced By The Tree Yshueeh'
'The Meaning Of Life As Found Through The Gematria'
'The Tree Of Life And Tree Of Knowledge Are The T W I'
'Jesus Christ The Way Truth And The Light Life'
'I Am The Way The Truth And Life Mdm Lion'
'Alejandro Enrique Palma Campain Born The Fifth Of'
'God Send Your Second Coming Before It Is Too Late'
'Jerusalem Living Sacrifice'
'Alex Enrique Palma Campain Born The Fifth Of May'
'The Extrum Cost Of The Jewish Order'
'Alex Enrique Campain Born The Fifth Of May'
'Yeshua My Soul Belongs To You Am'
'Beast Worthy To Open The Book'
'The Fifth Of May'
'Jesus Reappears'
'The Cia Knows Alejandro Campain Gematria Stats And They Are Scared'
'Iesus Hominum Salvator'
'Jesus Rey Christ Lst'
'Alejandro Campain Born The Fifth Of May'
'The Mayor Jesus Christ Of Peace'
'I Am Avenging The Voice Of God'
'Gods Code Translation Perfected Gene'
'The Most Godly Woman Ever Born'
'The Christ Aec'
'What Is The Meaning Of Jesus And Alex Campain'
'Christ Aec'
'Infinite'
'God Particle'
'The God Particle'
'Peaceful Warriors'
'Alpha God Particle'
'The Hidden'
'All In One'
'What Is The Meaning Of The Gift'
'Prayer De Guadalupe'
'Mary And Christ And Abba Yhwh We Rock Backs'
'Alejandro E Campain Born The Fifth Of May'
'Alexander E Campain Born The Fifth Of May'
'I Am Coming For You At The Rapture'
'Jesus Is Coming To Take You Home'
'The Prophet Warned'
'The True Jesus Christ Repentance'
'Yeshua Wanting It'
'Alexander Enrique Campain Born The Fifth Of May'
'The Self Esteem Yahweh'
'The Gematria Of Awakening Consciousness'
'Yeshua Christ Goes Savior'
'Jesus Christ Is A Sinner'
'The Anointed Twins'
'Yahweh Yehovah Father Of Truth'
'Decode The Spirit Soul Birth Are'
'Alexander Campain Born The Fifth Of May'
'Decode The Cia Is Scared Of Jesus Christ'
'Angel Of Jehovah'
'The Divine Alignment Gematria'
'Jackie On The Cross'
'Our Groove Has A Message For You'
'Manifestation Of Love And Light'
'Yeshua I Know That You Returned'
'The Lord Savior Christ Of Jesus'
'Lexus Is A Jesus'
'Jesus Christ God Is A Sinner And His Name Is'
'Jesus Gematria Decipher'
'Alex E Campain Born The Fifth Of May'
'A Who Are The Two Witnesses'
'The Ancient Has Awakened'
'Jesus Every Cross Doing Horse'
'The Triple Eight Green Is Sacred'
'The Lord And Savior King Our Bright Morning Star'
'Jewish Gematria Calculator'
'Are Jesus Of Nazareth Living Son Of See Of God'
'Am Son Of I Jesus Of Nazareth Living Son Of God'
'The Lord Savior Alexandro E Palma Campain'
'Jesus Christ Is The Only Way Truth And Life'
'Almighty Jesus Is Eternal In Eternal Hall'
'The Lord Savior Alexander Enrique Palma Campain'
'The Lord Savior Alexandro Enrique Palma Campain'
'Our Lord Savior Alexandro Enrique Campain'
'Our Lord Savior Alexandro Enrique Palma Campain'
'Thee Lord Savior Alexandro E Campain'
'Thee Lord Savior Alexandro Enrique Palma Campain'
'Thee Lord Savior Alexandro Campain'
'Thee Lord Savior Alexandro Enrique Campain'
'Jesus Christ Was Born The Fifth Of May'
'Jesus Christ From The Fifth Of May'
'Decode Jesus Christ Was Born May Fifth'
'Decode Jesus Christ May Fifth'
'John Twelve Forty Four'
'John One Two Four Four'
'Psalms Seventy Three Jesus Christ The Return Of Our Savior'
'Psalm Twenty Three Psalm Jesus Christ The Return Of David'
'Our Lord E Campain Born May Fifth Nineteen'
'Our Lord Alex Campain Born May Fifth Nineteen'
'Jesus Christ Was Born The Fifth Of May Nineteen Seventy'
'Yeshua Christ Was Born The Fifth Of May Nineteen'
'Yeshua Christ Was Born May Nineteen Seventy Two At One Forty Am'
'Thee Lord Alexandro E Campain Born M'
'Yeshua Christ Was Born May Nineteen'
'Yeshua Christ Born The Fifth Of May Nineteen'
'Our Savior Alex Campain Born May Fifth Nineteen Seventy Two One Forty Am'
'Our Savior Alex Enrique Palma Campain May Fifth Nineteen Seventy Two At One Forty Am'
'Jesus Christ Our Lord Was Born The Fifth Of May Nineteen Seventy Two At One Forty Am'
'Jesus Was Born The Fifth Of May Nineteen Seventy Two'
'Yeshua Real Was Born The Fifth Of May Nineteen Seventy Two At One Forty Am'
'John Twelve Four Four'
'June Twelve Forty Four'
'Our Lord Alexandro E Campain Born Fifth Nineteen'
'Jesus Cried Out With A Loud Voice Father Into Your Hands I Commit My Spirit'
'Find Out When And Where The Messiah Was Born Is Born In The Future Past Or Present Me'
'Our Lord Alexandro E Campain Born May Fifth Nineteen Seventy Two At One Forty Am'
'Her Ac May'
'Am May'
'Hes King Ac'
'He Is Our Alex E Campain'
'For God So Loved The World That He Gave His One And Only Son That Whoever Believes In'
'Hola Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth'
'Christ Yeshua And Mighty Jesus Comes'
'The Son Of Christ And Number Struggles'
'You Are Of This World I Am Not Of This World'
'El Es Nuestro Savior Alex Enrique Palma Campain'
'Yeshua Ha Yhwh'
'Meaning Yeshua Is Ha Yhwh People'
'He Is Beginning To Look A Lot Like Christmas'
'El Es Nuestro Savior Alex E Campain'
'El Es Nuestro Savior Alex F Campain'
'El Es Nuestro Savior Alex Campain'
'El Es Nuestro Alex E Campain'
'Just Top Blend S'
'Porque De Tal Manera Amó Dios Al Mundo, Que Ha Dado A Su Hijo Unigénito, Para Que Todo'
'El Es Nuestro Savior Y El Rey, Alexandro Enrique Palma Campain, Nacido El Viernes Cinco De'
'Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth Nineteen'
'He Is Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth'
'He Is Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth Nineteen'
'He Is The Lord And Savior Our King Alexander Enrique Palma Campain Born Friday May Fifth Nineteen'
'Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth Nineteen Seventy Two At One Forty Am'
'Our Lord And Savior Alex Enrique Palma Campain Born Friday May Fifth Nineteen Seventy Two'
'The Blood Lines'
'The Blood Line'
'Da Vinci Secret'
'He Is The Lord Aec'
'Imparity'
'The Healers'
'The Rh Negatives'
'Catholic Church'
'Mr Jesus'
'Flower Of Life'
'God Is The Force'
'God Is With Me'
'Roman Catholic'
'The God'
'I Know Coded Language'
'Dot'
'The King Is Coming'
'The Final Battle'
'I Am King Is Coming'
'The Lion King'
'I B B M'
'Son Of Satan'
"What Is The Meaning Of Alex Enrique Campain'"
'Judgment Day'
'Lord Of Love'
'In Shape Of A Body'
'Finalis Ludi'
'Rewards System'
'The Ghost Aec'
'Miracles Happen'
'Lord God Is Here'
'The Lost One'
'Give God'
'Blessed Is God'
'Blessed By God'
'House Of Bread'
'Periodic Table'
'Tree Of Life'
'Gods Birth Code'
'Star Of David'
'King Jesus Bible'
'Middle Path'
'The Gods Code'
'The Gods Code Of God'
'On The Face Of The Earth Je'
'Your Jesus Christ'
'Lord Alex Campain May Fifth'
'Simulative Theory'
'The Unknower Of The King'
'The Lord Is My Shepherd I Shall Not Want'
'I Am Honored Christ The King I Am The Alpha And Omega The First And The Last'
'In The Beginning Was The Word And The Word Was With God And The Word Was God'
'The Bright And Morning Star'
'The Image Of The Invisible God'
'Jesús Descendit De La Cruz A Las 50 00'
'Jesús Oloroso De La Muerte'
'As Oor Dan Bor Hec May Sec MKL'
'Rey Jesus, El Hijo Del Adiosista Que Pueden'
'Soy Dios Tengo El Mismo Poder Que Jesús Y Tu May'
'You God Is Sitting On His Throne That You May Return To My Sacred Comfort'
'Christian Substance'
'The Only One God'
'Holy Holy Shekinah'
'The Second Coming Of Jesus Christ Left Sofiablo'
'Your True Father'
'Lord Of Story'
'Lucifer Gates'
'Gods Perfect Number'
'The First And The Last'
'Moon Fith Yod He'
'The Aleph Tau'
'Jesus Kyrios'
'Alex Campain Birth'
'Gematria Org'
'What Is The Meaning Of Life Alex Enrique Campain'
'Hidden History'
'Let There Be Light'
'Humble And Meek'
'The Fold Crosses'
'God The Father'
'Radi Hackanah'
'The Greatest Teacher'
'Intercession Of God'
'The Christ Force'
'Yeshua Lod Statistic'
'One Source Plant And Seed And Everything In Between'
'The Fairy Flavors Hearts Love Wine'
'Something Good Is Going To Happen'
'Ah Is Flower See Jesus'
'Alex Enrique Campain is God YHWH Jesus Christ'
'Thirteen Is Gods Number'
'Alex Enrique Campain Birth'
'Satan Code'
'Twelve Tribes Of Israel'
'Permit Blood Of Christ'
'I Am Colour'
'The Kingdom Of Heaven'
'Alex Enrique Campain Birth Month Of May Day The Fifth year nineteen Seventy two'
'What Is The Meaning Of Alex Enrique Palma Campain May Fifth Nineteen Seventy Two at One forty AM'
'The Mouth Of Apocalypse'
'I Am The Lily Of The Valley'
'The Birth Information Of Jesus Christ'
'The Lord And Shepherd'
'Yeshua Will You Send Me A Message'
'The King And Savior'
'The Anti War Jesus'
'The Most High Is The Sun At Rize'
'I Am Most Powerful Angel On Earth'
'I Love Jesus Christ Yall Better Worship'
'Yeshua Are U Really Your Bride'
'Come With Sweet'
'Alex Enrique Campain Born May Five'
'Jehovah Yireh Sabbath The Renewerge'
'The Blessing Of Abraham Comes Upon You'
'The Whole Duty Of God'
'Canonical Gospels'
'The King And I AM IAM'
'The Canonical Gospels'
'The Four Canonical Gospels'
'Our Lord And Savior Alex'
'Our Lord And Christ Aec'
'Golden Proportion Of God'
'Hidden From Your Eyes'
'Who Is The Son Of God'
'Our Lord And Goliath'
'Thoth Fif Ty Three'
'Thee Lord Christ Aec'
'Lord Christ Aec'
'Jewish Indeed'
'Blessing Of God'
'God Came To Earth'
'Priesthood'
'John Fifteen Three'
'In Jesus Christo I Pray Every Child'
'May Fifth One Nine Seven Two One Forty'
'Three God Alex E Campain'
'The Risen Savior'
'The Christ Proof'
'How Much Is The Christ Proof In Gematria? What Is The Meaning Of'
'Three God Alex Campain'
'Calculate Gematria'
'The God Risen'
'Thee New Chosen'
'Is Lord Alex Campain'
'Is Messiah Alex E Campain'
'The Mystic Numbers'
'Jesus Did Resurrect'
'Jesus Is Resurrection'
'Lord Yeshua Christ'
'The Sleeper Has Awakened'
'Child Of The Trinity'
'Lucifer Is The Hidden God'
'Awakening The Son Of God'
'The Bringer Of Light'
'The Promised One'
'The Flower Of Life'
'Thee End Area Prophecy'
'The Happily Ever After'
'Davids Second Coming Of Jesus'
'Three End Area Lordyes Campain'
'Christ Consciousness'
'Jesus Esoteric Saint'
'Social Security Number'
'You Are The Annointed One'
'The Second Coming Of Christ'
'The Final Mystery Revealed'
'Jesus Christ Second Coming'
'The Re Incarnation Of Christ'
'Reincarnation Of Christ'
'El Cristo Alex Campain'
'The Holy Law Of One'
'My Life Member'
'Jesus Christ End Game'
'The Seven Laws Of God'
'Lord Jesus Christ'
'Lord Paden Christ'
'Quantum Physics'
'God Shed His The World'
'The Ten Commandments'
'Christ Rapture Day'
'Soc Tele Plame Mewleth'
'Christmas Day'
'The Nicolaitans Campain'
'The Royal Holy Bloodline'
'You Are The Appointed One'
'The Second Coming Of Jesus'
'He Is Our Alex E Campain'
'Hes Our Alex E Palma Campain'
'I Am The Judge Of The Living And Dead'
'The Reptilian Light Reapers'
'True Revolution From God'
'Savior Of Man'
'He Is Alexandro Campain'
'Bible Of Christ'
'Virgin Mary'
'To Infinity In A Song'
'The Hollowed Hymns Of God'
'Jesus Christ Is King'
'The True Meaning The One'
'Revelation Twelve'
'The Real Jesus Christ'
'Iron Alex Enrique Campain'
'King Force Inverse'
'The Harvest Antichrist'
'Survey Mappe'
'He Is Alex Enrique Campain'
'Alejandro Campain Born May Fifth Nineteen'
'IAM The  Embodiment Of God'
'I Am The Son Of Man Y H V H I Come In My Fathers Name Jehovah'
'Truth Code Truth Code Truth Code Truth'
'Alejandro Campain May Fifth Nineteen'
'Yeshua Ha Mashiach New Jerusalem Abundance'
'The Bloodline Of King David Is At The Right Hand Where The Rivers Come Together'
'Miracles Are Light Of The Lord Jesus Christ With In'
'Theowrthy Numberin Search Results To Intercept'
'The Messiah Is Alive Today And Lives As You Right'
'King Jesus Queen Mary King Jesus Queen Mary King'
'Lord Please Help Me My World Rreak S S S'
'OOOOOOOOOOOOOOOOOOOOOO'
'Alexander Enrigue Campain S Birthdate May Fifth Nineteen Seventy Two'
'As H Hr Cel Put It The D D May Be One On One P'
'Vhodi Yekom Kodesh'
'Always Know Your Thinking'
'For The Son Of Man Is Lord Even Is To Come The Sabbath Was Made'
'The Rupture Of The Church Is About To Happen'
'The Lord Shall Repay You And To His Next Year'
'You Are The Second Coming Of Holy Bride Of Jesus'
'All Sins Are Vices That Are Answered To Sender'
'Kind David Der Fh rer Gottes Segen Dir Mit Deinem Des'
'Jesus Osborne Savs'
'Is God Real Identity'
'The Holy Resurrection'
'Jesus Osborne Savs Inc'
'Jesus Divine Bloodline'
'All Numbers Align In A Sign'
'I Believe In Yesh Jehovih The Father Of My Spirit'
'I Must Never Claim To Be Jesus Though I Am A'
'Holy Holy Holy Is The Name Of The Lord'
'Holy Holy Holy Is The Name Of The Lord Yehovah'
'Thee King Of Kings Will Reign Over The Kings Of The Earth'
'God Is Real Jesus Is Real And So Is The Holy Spirit'
'Jesus Christ Interfacing His Internal For Glory Of God'
'Adonai Svotcheovt The Wrhoel Ootpoint Is Adored V H'
'The Salvation Of The Lord Mean God Needs You To'
'Asian Yehoshuah'
'Ancient History'
'Christ Comes Tomorrow'
'How Much Is Asian Yehoshuah In Gematria? What Is The Meaning Of'
'Jesus Is The Flesh'
'The Creator God'
'The Creature God'
'I Am Here To Save All Souls And Take Us Even Into'
'Alex Campain Born May Fifth Nineteen Seventy'
'The Revelation Of Jesus Christ To John The Baptist'
'I Love You Father And I Give You My Full Armor'
'From The Side Of God Comes The Voice Of The Living God'
'He Is The God And The Living God Is God'
'The Name Of God Is God Jesus Christ Be With You All Amen'
'The Reason For Everyone And Everythings Existence'
'Jesus Shares The Bloodline Of Jesus Christ'
'The Love Of My Life'
'The Holy Marriage Feeds God'
'Decode The Christ Pearl'
'Decode Jesus Calculator'
'Chosen Messenger Of God'
'You Are So Beautiful'
'Sacred Coming Of Jesus'
'The Lord Slays On You'
'The Truth Of Gods Word'
'Soulsils Of Mary Magdalene'
'I Am The Alpha And Omega'
'Behold The Lambs Of God'
'The Second Coming'
'The Antichrist'
'Lions Of Israel'
'I Am The Chosen One'
'Chaos Is Risen'
'Lucifer Christ'
'Infinity'
'How Much Is Infinity In Gematria?'
'He I Alejandro Campain'
'He Is Alex E Campain'
'Cristo Alex E Campain'
'The Holy Grail'
'How Much Is The Holy Grail In Gematria? What Is The Meaning Of'
'Lucifer'
'How Much Is Lucifer In Gematria?'
'He Is A King Campain'
'Hes Hes K Alex E Campain'
'Is Alex Campain'
'Here Comes The Son'
'Baruch Hashem Adonai'
'In Name Alexandro E Campain'
'A Lord Alex Campain'
'John Psilocybin'
'Hes Our C Alex E Campain'
'What Is My Mind Is'
'What Is Decoded In The Bible'
'Saint Michael The Archangel'
'Decode Jesus Prophecy'
'Message From God Urgently Imparted'
'Satan Lucifer God'
'Fat Arse'
'Jesus Arrival',
'Fat Arse Logger'
'Thank You Lord'
'The Morning Star'
'He Alexander Campain'
'I Am The Angel Of Death'
'This Is Yehovah'
'I Am The Prophet'
'Mary Magdalene Revealed'
'Return Of The King'
'Jesus Christ'
'I Am The Man Of Purity And Holy Spirit'
'Who Is The Adam'
'Where The Adam'
'Her Alejandro Campain'
'Her Alex E Campain'
'Her Alejandro E Campain'
'He Sent Yes'
'Hesed'
'Hosanna'
'How Much Is Hosanna In Gematria?'
'He Is The Lord Alex'
'He Is King Aec'
'Baruch Hashem'
'The Christ The Son Of The Living God'
'Hebrew Gematria Calculator'
'He Is Thee Messiah'
'He Alejandro E Campain'
'He Alejandro Campain'
'He Is The Holy Mashiach'
'He Is Thor Mashiach'
'Yahweh'
'Warlock'
'He Is Spoken Fifty Three'
'Lucky Fifty Three'
'King Alex E C Campain'
'The Book Of Soul'
'Prophet Of God'
'King Alex E Campain'
'One True God'
'How Much Is Masturbating In Gematria?'
'Code Birth Date'
'Revelation'
'New Years Day'
'Soulmate Of Mary Magdalene'
'The Synagogue Of Yeshua'
'You Are Faithful And True'
'Jerusalem Israel'
'In My Fathers House Are'
'Patience Of Jesus To Stack The Lord'
'Holy Feminine Side Of The Sister'
'Mary Magdalene And Jesus Christ'
'In Defendo Dei Is Jesus'
'Shift Out Of False Reality'
'The Messiah'
'How Much Is Son Of David In Gematria? What Is The Meaning Of'
'Son Of David'
'Our Angelic Campain'
'How Much Is Son Of David In Gmatria?'
'Christ Jesus'
'God Word Of Faith'
'The Children Of Israel'
'Decode Jesus Arrival'
'I Am In These Hands'
'Society Of Jesus'
'Twin Flames Unite'
'Yo, Señor Y Salvador, Alex Campain, Messiah El'
'Thee Lord And Savior Alex Campain Born Friday May Fifth Nineteen Seventy Two'
'Holy Yeshua'
'Our Holy Lord Yeshua Christ Is Alex Enrique Campain',
'Are Thee Lord And Savior Alex Campain Born Friday May Nineteen Seventy Two'
'The Lion Of Judah Alex Campain Born May Five Nineteen Seventy Two One Forty Am'
'Thee Lord And Savior Alex E Campain Born Friday  May Five Nineteen Seventy Two'
'Soy Yo, Señor Y Salvador, Alex Campain, Messiah El'
'Thee Lord Savior Alex E Campain Born Friday May'
'Our Lord Jesus Alex E Campain Born Friday May Nineteen Seventy Two One Forty Am'
'But Whosoever Shall Deny Me Before Men Him Will I'
'Thee Lord Alex E Campain Born Friday May Nineteen Seventy Two One Forty Am'
'The Lord Alex E Campain Born Friday May'
'Matthew Ten Three Three'
'Matthew Ten Thirty Three'
'Alejandro Enrique Palma Campain May Five Nineteen Seventy Two’,'
'I Am The Way The Truth And The Life No One Comes Fa'
'Aec'
'Hackers'
'He Is A God Aec'
'Ac And Love'
'Satan'
'May Fifth'
'The Message That Will Change Your Life'
'I Am Coming And I Shall Dwell In Your Midst'
'The Bright Morning Star'
'El Salvador Aec'
'Palm Sunday'
'How Much Is Palm Sunday In Gematria? What Is The Meaning Of'
'Domingo De Ramos'
'The Savior Aec'
'The Holy Spirit'
'Savior Aec'
'Lord Alex Campain'
'How Much Is Palm Sunday In Gematria?'
'Yo Escribí La Historia'
'Yhwh Escrib La Historia'
'Alexander Campain Y Viernes Cinco De Mayo De Mil Novecientos Setenta Y Dos, Uno Cuarenta A M'
'Born On Friday The Fifth Of May Nineteen Seventy Two'
'Born On Friday The Five Of May Nineteen Seventy Two At One Forty Am'
'I Was Born On A Friday May Fifth Nineteen Seventy'
'Born On A Friday May Fifth Nineteen Seventy Two At'
'Yeshua Christ Our Lord And Savior Born On This'
'Jesus May Fifth Nineteen Seventy Two At One Party'
'At Don Fifth Of May Nineteen Seventy Two At One'
'As Don Fifth Of May Nineteen Seventy Two At One'
'C Don On May Five Nineteen Seventy Two At One Party'
'Born On Friday May Fifth Nineteen Seventy Two At One'
'A Birthdate May Fifth Nineteen Seventy Two At One'
'E Birthdate May Fifth Nineteen Seventy Two At One Party'
'Birthday May Fifth Nineteen Seventy Two At One Party'
'A Friday May Fifth Nineteen Seventy Two At One Party'
'Yeshua Christ Our Lord And Savior Born On This Day'
'Jewish Day'
'John Fourteen Six'
'Is Alexandro E Campain'
'Venus Love Angel'
'I Accept The Holy Spirit Ac'
'Thank You For Being You'
'Jehovah I Will Go For You'
'I Am Proud Of Who I Become'
'The Joy And The Grace'
'Jesus Project'
'Supernatural Abilities'
'Jesus Christ Revealed'
'Born Again Is Jesus Project In'
'Greater Than You Think'
'No One Know This Secret'
'Yeshua Keeper Of The Dragon'
'Chosen Pleiadeans Of Christ'
'House Of The Rising Sun'
'Aec May Fifth Seventy Two'
'The Royal Blood Jesus'
'Thee Lord And Savior Alex Campain Born Friday May Fifth Nineteen Seventy Two One Forty Am'
'La Noche Del Espíritu Santo'
'Alejandro Enrique Campain Mayo'
'Cristo De Templo'
'Ay, Mismo, Señor, Alex, Campain,'
'Cristo Alex Campain'
'Yo, Mismo, Señor, Alex, Campain,'
'Mateo Diez Treinta Y Tres'
'El Salvador Y La Sangre De Cristo Jesus El'
'The Lord And Savior Alex E Campain Born Friday May'
'Yo, Señor, Y Salvador, Alex Campain, Messiah El'
'Zechariah One Four'
'He Is The Lord King Aec'
'Zechariah Fourone'
'Zechariah Fourteen'
'Zechariah One Five'
'Zechariah Fourteen One'
'Zechariah Fourteen One Through Five'
'Zechariah One Four Overdue'
'The Manifestation Of God'
'Unconditional Love'
'Jesus Christ Of Nazareth'
'Alejandro Enrique Campain May'
'Thee Messiah Lord Alex E Campain'
'Jupiter Symphony'
'The Biblical Son Of God'
'In Jupiter Symphony'
'A Divine Frequency'
'Ark Of The Covenant'
'God Is Hidden In Our DNA'
'The King Alex E Campain'
'Bloodline Of Jesus'
'Alex Campain'
'The Holy Trinity'
'Jesus Answer'
'On The Final Countdown'
'Seconds Second Coming Of Jesus'
'Jesus Returns Soon'
'Fresh Point From The Sky'
'Social Security Numbers'
'Zechariah One Through Five'
'The Last Prophet'
'Jesus MMXCIX'
'Destined Past Life'
'Chosen By God'
'Thou King ART Alex E Campain'
'The Holy Great One'
'Da Vinci Code'
'My Name'
'Gods Human Horse'
'Real God Code'
'Alexandra'
'I Love God'
'Purify Your'
'Enrique'
'Gift Of God'
'Religion'
'Chosen Blood'
'Jesus Heals'
'Holy Flame'
'King Of Kings'
'Totality'
'Twinflames'
'The Torah Code'
'Jesus Christ Of The Son'
'Thee Lord And Savior Alex Campain'
'The One Worthy Of Almighty God'
'How Much Is The One Worthy Of Gematria?'
'I Am Haqqamshi Christ The King I Am The Alpha And'
'Christ Returns V Years Ahead Of Schedule'
'In Lord Jesus Christ Name Free Every One'
'Decode Yehovah And Yehoshua Aman'
'I Have The Lord Jesus Christ'
'All Frequencies And Timelines Align'
'Thee Lord And Savior Alex E Campain'
'Word Of Christ'
'His Only Begotten Son Christ'
'The Yahya Spell All Ah Wh Ah'
'Our Lord And Savior Alex Campain'
'I Am In The Captain Of Our Salvation'
'The Creative Story Ever Told'
'Deep Reminders Of True Reality'
'The Revelation Of Jesus Christ'
'King David Reincarnated Has Returned'
'The Second Coming Of Jesus Christ'
'Yeshua Is Yahweh'
'Jesus Christ Four Four Four'
'Jesus Christ Of The Utterance'
'The Harmony Of Love Jesus'
'Jesus Christ His Teacher'
'An Je Hovih To Stay Back K J'
'Manifested Physical Representation Of Logos'
'Interplanetary Currency'
'I Am The Life Of The Valley'
'Thee Lord And Savior Aec'
'The Tenth Commandment'
'Angel Of Yahweh'
'He Is Immanuel To Yeshua'
'Jesus Family'
'The Lord And Savior Aec'
'The Voice Of Motoneuron'
'The Only One The Lord'
'In A New Body'
'My New Name'
'Sealed Am'
'Sons Of God'
'The Source'
'Frequency'
'Convention'
'Birthday Code'
'How Much Is New World In Gematria?'
'New World'
'Ye And Yang'
'Yin And Yang'
'New Earth'
'Tokyo'
'Being His Divine Teacher'
'Crucifixion Is Horrible Man'
'El Elyon'
'Gevurah Am'
'May Am Fifth'
'King Am May Fifth'
'The Promised Land'
'The Light'
'The King Aec'
'He Man'
'Of War'
'Gematria'
'Input'
'True Ape'
'Alex'
'Five'
'How Much Is Alex In Gematria?'
'The Aec'
'Cain'
'Aqos'
'Elleven'
'Flores'
'Easter'
'Sagiso'
'The Lord Aec'
'Say Love Aec'
'Triple Eights'
'Lion Of Judah'
'The 13 Satanic Bloodlines'
'You Are A God'
'Shakti'
'Shaddai El Chai'
'Last Am May'
'Aqos May Five'
'Houston'
'Decode The Lord'
'King Aec May Five'
'Jesus God Son'
'Aec May Fifth'
'The Lord Of God'
'Sunday'
'Saturday'
'Yehoshua'
'Gate Of Rock'
'Fifty Five'
'Not Everyones Who Says To Me Lord Lord Will Enter The'
'Thee Lord And Savior Alex E Campain Fifth Nineteen Seventy Two At One Forty Am'
'Thee Lord Alex E Campain May Fifth Nineteen Seventy Two At One Forty Am'
'Has Thee Lord Alex E Campain May Fifth Nineteen Seventy Two At One Forty Am'
'Dat M C Born May Fifth Nineteen Seventy Two At'
'As Lord Savior Born May Fifth Nineteen Seventy Two At One Forty Am'
'Thee Savior Born May Fifth Nineteen Seventy Two At'
'Thee Savior Born May Fifth Nineteen Seventy Two At One Forty Am'
'Dat Savior Born A May Fifth Nineteen Seventy Two At One Forty Am'
'H Lord J Born May Fifth Nineteen Seventy Two At'
'Our Jesus C Born May Fifth Nineteen Seventy Two At'
'Lord C Yeshua Born May Fifth Nineteen Seventy Two At One Forty Am'
'Immaculate Birth May Five Nineteen Seventy Two At'
'Lord C Yeshua Birth May Fifth Nineteen Seventy Two At'
'Immaculate Birth May Five Nineteen Seventy Two At One Forty Am'
'Yeshua Christ Of Nazareth Our Lord And Savior Was Born On This Day'
'Born A Friday May Fifth Nineteen Seventy Two At One'
'The Lord Born A Friday May Fifth Nineteen Seventy Two At One Forty Am'
'I Jesus Born Friday May Fifth Nineteen Seventy Two At'
'Count The Number Of Letters In Your Name'
'You Cheated On Her She Will Cheat On You'
'Our Lord Savior Alexandro E Campain'
'Our Lord Savior Alexandro Campain'
'Christo Return As A Lion Fulfilled'
'Yah Mhe Can Do This Is It Just I'
'Jesus Christ The Conquering Lion Is Back'
'I Am The Way The Truth And The Life Indeed'
'The Antichrist Is Return With Ai'
'Your Daddy Is Yahweh'
'You Are A Beautiful Flower Of Christ'
'You Are Absolutely One Of The Kind'
'If Yeshua Knew'
'I Am The Second Coming Of Jesus Christ'
'The Four Corners Of The Yhwh'
'The Lord Of Hosts Is With Us'
'The Four Corners Of The Earth'
'The Sacred Geometry Of The Human Body'
'Thee Lord And Savior Alexandro Campain'
'The Way Kadosh Is Jesus Christ'
'The Full Armor Of God Protection'
'I Have Chosen You Out Of The World'
'Jewish Month Of The Spirit'
'April Showers Bring May Flowers'
'Is Heavenly Worth My Efforts'
'The Whimsical Periods Of Existence'
'Jesus Is Coming To Save His People'
'I Am The Lies That They Want To Kill'
'Jesus Reincarnation Reborn'
'Bible Code Your Name And See What It Means'
'He Is My God Symbol Apocalypse'
'Holy Spirit Sanctifier'
'Ability To Change The World Stone Game'
'The Savior Jesus Christ The Lord'
'Jesus Is It Verrines Melaon Cadmon'
'Bring Alive Is Terrible Thanks A Lot God'
'The Second Coming Of Jesus Will Be Hated'
'He Is The Christ And He Is Alive Among Us'
'Christ With White Hair And Sword'
'God God God God God God God God God God God God God God God'
'What Is Name Of The Soul Of Salvation'
'White Jesus'
'Thee Lord Savior Alexandro E Campain'
'Im Black And I Turn Water Into Dcil'
'Praye Me Wrong'
'Gematria Is God Je'
'See What Is Good For Je'
'Negro Yeshua Two Has Returned'
'Thee Hidden One Is Christ H'
'Four Horsemen Of The Apocalypse'
'The Great Architect Of The Universe'
'Children Celebration Of Almighty God'
'Five Times Facter Radio Frequency'
'Decode If He Holy Son Of Almighty God'
'The True Bride Of Christ End Of Church'
'Messiah Lives In United States F B I'
'The Return Of Jesus Of Nazareth'
'The Divine Child Is The Chosen Son Of God'
'Thee Lord Alexandro E Campain'
'You Are The Reincarnation Of Lucifer'
'One Hundred Forty Four Thousand'
'A God Jesus Christ Go Down'
'I Jesus Christ Will Go Down'
'Reincarnation Of Jesus Christ I Am Back'
'Thee Lord And Savior Alexandro E Campain'
'Inverse Ondhas Rec'
'Oh Good God Jesus Lives So Be It'
'Thee Lord And Savior Alexandro Enrique Campain'
'Thee Lord And Savior Alexandro Enrique Palma'
'I Am The True Vine And My Father Is The Vine Dresser'
'The Twenty Six Letters Of The English Alphabet'
'The Holy Spirit The Final Call Before The Apocalypse'
'The Second Coming Of Jesus Are United'
'Thee Lord Savior Alexandro Campain'
'The Most Important Gematria Code'
'The Quantum Still Repentance'
'The Important Return Of The Lord'
'People Also Ask'
'Messianic Seamless Garment'
'Be The Second Coming Of Jesus Christ'
'I Amnot With You'
'Not Much Time Left To Choose Jesus'
'Selfish Reasons'
'Infinitely Serve On TheLord'
'You Are Second Coming Of Holy Bride Of Christ'
'The Numbers Of Your Name Meaning'
'The Son Of David Jesus Christ'
'Who Is Yeshua In The Flesh'
'You Really Are The Second Coming Of Christ'
'Jesus Christ King Of Kings And Lord Of Lords'
'Jesus The Christ The Lords Holy Code'
'I Am A God Je'
'Annointed Messenger Of Lucifer'
'Immanueljehosua'
'How Much Is Decode Our Souls'
'Decode Our Souls Belongs To Him'
'The Annointed King Of The Davidic Line'
'Divine Creation Jesus Messiah'
'I Am True Prophet Sent By God'
'Holy Translation Of God Codes'
'Our Lord And Savior Jesus Christ'
'Jesus Christ Was A Normal Man'
'Jesus Christ Protects Little Children'
'The Most Powerful Triple Digit Number'
'The Math Behind The Letters Of The Alphabet Encoded'
'Y O U Are The Only One True Who I Am'
'The Dragon That Will Come True'
'The Holy Spirit Lives Within This Man'
'Jesus Didn T Write Come True'
'Jesus A Walk Come True'
'Holy Jesus Above And Kind'
'Holy Miracle Walking'
'Holy Holy Holy Is Lord God Almighty'
'Our Lord And Savior King The Morning Star'
'Our Lord And Savior King Theo Bright Morning Star'
'He Is Our Lord And Savior The Bright Morning Star'
'He Is Thee Lord And Savior King The Bright Morning'
'He Is Thee Lord And King The Morning Star'
'He Is Thee Lord And Savior King The Morning Star'
'The Queen Of The Five Sins Is The Son Of Man'
'The Lord And King The Bright Morning Star'
'Loved By God'
'The Universe'
'How Much Is The Universe In Gematria?'
'Allah Allah Allah Allah Allah Allah Allah Allah'
'The Divine Wrath Of YHWH'
'Lord God Almighty Straight Up Jesus'
'Lord God Almighty Christ Is Risen'
'I Am God I Have Returned Age Of Aquarius'
'Jesus Of Nazareth King Of The Jews'
'The Divine Name Of Almighty God'
'Jesus Christ Is A White American Male'
'The King The Bright Morning Star'
'Universal Divine Law'
'Gods Plan'
'Holy Trinity Of Planet Heaven H H H'
'Your Jesus Christ Is The Savior'
'Our Lord Savior Alex Campain'
'Our Lord Savior Alex Enrique Campain'
'God Is Talking To You Via Car License Plates'
'I Love Yahweh Elohim'
'All The Worlds A Stage And All The People Players On'
'Gematria Proves The Words Youall Choose'
'Catholicism Is A Percentage Of Jesus Teaching'
'The Messiah Is The Christ And The Antichrist'
'Holy Spirit Of The Lord God Me I Love You'
'Jesus Christ Is Real Not A Myth'
'DREAMORGASMDEATHORDREAMORGASMDEATHOR'
'The Son Of God Is Amongst Us The Light Is Here'
'Jesus Died On A Cross To Overcome Sin'
'Yes Have Heard God Is Real Po'
'Thee Lord Savior Alex Campain'
'The Cross Of Jesus Christ'
'Yahweh The Living God'
'Simple Reasons Messiah Jesus'
'Get Lord Savior Alex Enrique Campain'
'He Is Saving The Whole Universe'
'I Am Jesus'
'The King Who Is To Be The Bright Morning Star'
'Jesus Christ Returned Last Year'
'Thee Lord Savior Alexander Le Campain'
'Lucifer The Kings Ruler Other'
'I Am The Holy Spirit Be Aware Of Me And My Power'
'Who Is Lord Jesus Christ'
'Thee Lord Savior Alexander Campain'
'Our Lord Savior Alexander Campain'
'Thee Lord And Savior King Theo Bright Morning Star'
'The Lord And Savior King Theo Bright Morning Star'
'The Lord And Savior King Theo Morning Star'
'Lord And Savior King The Bright Morning Star'
'The Lord And Savior King Our Morning Star'
'Thee Lord And Savior King Our Bright Morning Star'
'The Star Of The Peace'
'Who Is Christ'
'He Is Our Lord And King The Morning Star'
'The Lord And King The Morning Star'
'I Am The Lord Your God'
'Thee Lord And King The Morning Star'
'Christians With A New Body'
'Three God Alex E Campain'
'The Risen Savior'
'What Is The Meaning Of'
'Three God Alex Campain'
'The God Risen'
'Thee New Chosen'
'Is Lord Alex Campain'
'Is Messiah Alex E Campain'
'The Mystic Numbers'
'Jesus Did Resurrect'
'Jesus Is Resurrection'
'Lord Yeshua Christ'
'The Sleeper Has Awakened'
'Child Of The Trinity'
'Lucifer Is The Hidden God'
'Awakening The Son Of God'
'The Promised One'
'Thee End Area Prophecy'
'The Happily Ever After'
'Davids Second Coming Of Jesus'
'Three End Area Lordyes Campain'
'Christ Consciousness'
'Jesus Esoteric Saint'
'Social Security Number'
'You Are The Annointed One'
'El Cristo Alex Campain'
'The Holy Law Of One'
'My Life Member'
'Jesus Christ End Game'
'The Seven Laws Of God'
'Lord Paden Christ'
'God Shed His The World'
'Christ Rapture Day'
'Soc Tele Plame Mewleth'
'The Nicolaitans Campain'
'The Royal Holy Bloodline'
'You Are The Appointed One'
'He Is Our Alex E Campain'
'Hes Our Alex E Palma Campain'
'I Am The Judge Of The Living And Dead'
'The Reptilian Light Reapers'
'True Revolution From God'
'He Is Alexandro Campain'
'Bible Of Christ'
'To Infinity In A Song'
'The Hollowed Hymns Of God'
'The True Meaning The One'
'Revelation Twelve'
'Iron Alex Enrique Campain'
'King Force Inverse'
'The Harvest Antichrist'
'Survey Mappe'
'Alejandro Campain Born May Fifth Nineteen'
'IAM The Embodiment Of God'
'Truth Code Truth Code Truth Code Truth'
'Alejandro Campain May Fifth Nineteen'
'The Bloodline Of King David Is At The Right Hand Where The Rivers Come Together'
'Miracles Are Light Of The Lord Jesus Christ With In'
'Theowrthy Numberin Search Results To Intercept'
'The Messiah Is Alive Today And Lives As You Right'
'Lord Please Help Me My World Rreak S S S'
'OOOOOOOOOOOOOOOOOOOOOO'
'Alexander Enrigue Campain S Birthdate May Fifth Nineteen Seventy Two'
'As H Hr Cel Put It The D D May Be One On One P'
'Vhodi Yekom Kodesh'
'Always Know Your Thinking'
'For The Son Of Man Is Lord Even Is To Come The Sabbath Was Made'
'The Rupture Of The Church Is About To Happen'
'The Lord Shall Repay You And To His Next Year'
'You Are The Second Coming Of Holy Bride Of Jesus'
'All Sins Are Vices That Are Answered To Sender'
'Kind David Der Fh rer Gottes Segen Dir Mit Deinem Des'
'Jesus Osborne Savs'
'Is God Real Identity'
'The Holy Resurrection'
'Jesus Osborne Savs Inc'
'Jesus Divine Bloodline'
'All Numbers Align In A Sign'
'I Believe In Yesh Jehovih The Father Of My Spirit'
'I Must Never Claim To Be Jesus Though I Am A'
'Holy Holy Holy Is The Name Of The Lord'
'Holy Holy Holy Is The Name Of The Lord Yehovah'
'Thee King Of Kings Will Reign Over The Kings Of The Earth'
'Jesus Christ Interfacing His Internal For Glory Of God'
'Adonai Svotcheovt The Wrhoel Ootpoint Is Adored V H'
'The Salvation Of The Lord Mean God Needs You To'
'Asian Yehoshuah'
'Ancient History'
'Christ Comes Tomorrow'
'How Much Is Asian Yehoshuah In Gematria? What Is The Meaning Of'
'Jesus Is The Flesh'
'The Creature God'
'I Am Here To Save All Souls And Take Us Even Into'
'Alex Campain Born May Fifth Nineteen Seventy'
'I Love You Father And I Give You My Full Armor'
'From The Side Of God Comes The Voice Of The Living God'
'He Is The God And The Living God Is God'
'The Name Of God Is God Jesus Christ Be With You All Amen'
'Jesus Shares The Bloodline Of Jesus Christ'
'The Love Of My Life'
'The Holy Marriage Feeds God'
'Decode The Christ Pearl'
'Decode Jesus Calculator'
'You Are So Beautiful'
'Sacred Coming Of Jesus'
'The Lord Slays On You'
'Soulsils Of Mary Magdalene'
'Behold The Lambs Of God'
'Chaos Is Risen'
'How Much Is Infinity In Gematria?'
'He I Alejandro Campain'
'He Is Alex E Campain'
'Cristo Alex E Campain'
'How Much Is The Holy Grail In Gematria? What Is The Meaning Of'
'How Much Is Lucifer In Gematria?'
'He Is A King Campain'
'Hes Hes K Alex E Campain'
'Is Alex Campain'
'Here Comes The Son'
'Baruch Hashem Adonai'
'In Name Alexandro E Campain'
'A Lord Alex Campain'
'John Psilocybin'
'Hes Our C Alex E Campain'
'What Is My Mind Is'
'What Is Decoded In The Bible'
'Message From God Urgently Imparted'
'Satan Lucifer God'
'Fat Arse'
'Fat Arse Logger'
'Thank You Lord'
'He Alexander Campain'
'I Am The Angel Of Death'
'This Is Yehovah'
'Mary Magdalene Revealed'
'I Am The Man Of Purity And Holy Spirit'
'Who Is The Adam'
'Where The Adam'
'Her Alejandro Campain'
'Her Alex E Campain'
'Her Alejandro E Campain'
'He Sent Yes'
'Hesed'
'Hosanna'
'How Much Is Hosanna In Gematria?'
'He Is The Lord Alex'
'He Is King Aec'
'Baruch Hashem'
'The Christ The Son Of The Living God'
'He Is Thee Messiah'
'He Alejandro E Campain'
'He Alejandro Campain'
'He Is The Holy Mashiach'
'He Is Thor Mashiach'
'Warlock'
'He Is Spoken Fifty Three'
'Lucky Fifty Three'
'King Alex E Campain'
'The Book Of Soul'
'Prophet Of God'
'King Alex E Campain'
'How Much Is Masturbating In Gematria?'
'Code Birth Date'
'New Years Day'
'Soulmate Of Mary Magdalene'
'The Synagogue Of Yeshua'
'You Are Faithful And True'
'Jerusalem Israel'
'In My Fathers House Are'
'Patience Of Jesus To Stack The Lord'
'Holy Feminine Side Of The Sister'
'Mary Magdalene And Jesus Christ'
'In Defendo Dei Is Jesus'
'How Much Is Son Of David In Gematria? What Is The Meaning Of'
'Son Of David'
'Our Angelic Campain'
'How Much Is Son Of David In Gmatria?'
'Christ Jesus'
'God Word Of Faith'
'The Children Of Israel'
'I Am In These Hands'
'Yo, Señor Y Salvador, Alex Campain, Messiah El'
'Thee Lord And Savior Alex Campain Born Friday May Fifth Nineteen Seventy Two'
'Holy Yeshua'
'Are Thee Lord And Savior Alex Campain Born Friday May Nineteen Seventy Two'
'The Lion Of Judah Alex Campain Born May Five Nineteen Seventy Two One Forty Am'
'Thee Lord And Savior Alex E Campain Born Fifth Nineteen Seventy Two'
'Soy Yo, Señor Y Salvador, Alex Campain, Messiah El Hijo Del Dios',
'Thee Lord Savior Alex E Campain Born Friday May'
'Our Lord Jesus Alex E Campain Born Friday May Nineteen Seventy Two One Forty Am'
'But Whosoever Shall Deny Me Before Men Him Will I'
'Thee Lord Alex E Campain Born Friday May Nineteen Seventy Two One Forty Am'
'The Lord Alex E Campain Born Friday May'
'Alejandro Enrique Palma Campain May Fifth Nineteen Seventy Two'
'I Am The Way The Truth And The Life No One Comes Fa'
'Hackers'
'He Is A God AEC' 
'Ac And Love'
'Satan'
'I Am Coming And I Shall Dwell In Your Midst'
'El Salvador AEC' 
'Palm Sunday'
'How Much Is Palm Sunday In Gematria? What Is The Meaning Of'
'Domingo De Ramos'
'The Savior AEC' 
'Savior AEC' 
'How Much Is Palm Sunday In Gematria?'
'Yo Escribí La Historia'
'Yhwh Escribe La Historia'
'Alejander Campain Y Viernes Cinco De Mayo De Mil Novecientos Setenta Y Dos, Uno Cuarenta A M'
'Born On Friday The Fifth Of May Nineteen Seventy Two'
'Born On Friday The Five Of May Nineteen Seventy Two At One Forty Am'
'I Was Born On A Friday May Fifth Nineteen Seventy'
'Born On A Friday May Fifth Nineteen Seventy Two At'
'Yeshua Christ Our Lord And Savior Born On This'
'Jesus May Fifth Nineteen Seventy Two At One Party'
'At Don Fifth Of May Nineteen Seventy Two At One'
'As Don Fifth Of May Nineteen Seventy Two At One'
'C Don On May Five Nineteen Seventy Two At One Party'
'Born On Friday May Fifth Nineteen Seventy Two At One'
'A Birthdate May Fifth Nineteen Seventy Two At One'
'E Birthdate May Fifth Nineteen Seventy Two At One Party'
'Birthday May Fifth Nineteen Seventy Two At One Party'
'A Friday May Fifth Nineteen Seventy Two At One Party'
'Yeshua Christ Our Lord And Savior Born On This Day'
'Jewish Day'
'Is Alexandro E Campain'
'Venus Love Angel'
'I Accept The Holy Spirit Ac'
'Thank You For Being You'
'Jehovah I Will Go For You'
'I Am Proud Of Who I Become'
'The Joy And The Grace'
'Jesus Project'
'Supernatural Abilities'
'Jesus Christ Revealed'
'Born Again Is Jesus Project In'
'Greater Than You Think'
'No One Know This Secret'
'Yeshua Keeper Of The Dragon'
'Chosen Pleiadeans Of Christ'
'House Of The Rising Sun'
'The Royal Blood Jesus'
'Thee Lord And Savior Alex Campain Born Prie Nineteen Seventy Two One Forty Am'
'La Noche Del Espiritu Santo'
'Alejandro Enrique Campain Mayo'
'Cristo De Templo'
'Ay, Mismo, Señor, Alex, Campain,'
'Cristo Alex Campain'
'Yo, Mismo, Señor, Alex, Campain,'
'Mateo Diez Treinta Y Tres'
'El Salvador Y La Sangre De Cristo Jesús El Señor',
'The Lord And Savior Alex E Campain Born Friday May'
'Yo, Señor, Y Salvador, Alex Campain, Messiah El'
'Zechariah One Four'
'He Is The Lord King Aec'
'Zechariah Fourone'
'Zechariah Fourteen'
'Zechariah One Five'
'Zechariah Fourteen One'
'Zechariah Fourteen One Through Five'
'Zechariah One Four Overdue'
'Jupiter Symphony'
'In Jupiter Symphony'
'God Is Hidden In Our DNA'
'The King Alex E Campain',
'Jesus Answer',
'On The Final Countdown'
'Seconds Second Coming Of Jesus'
'Jesus Returns Soon'
'Fresh Point From The Sky'
'Social Security Numbers'
'Zechariah One Through Five'
'Jesus MMXCIX'
'Destined Past Life'
'Thou King Are E Campain'
'Da Vinci Code'
'My Name'
'Real God Code'
'Alexandra'
'I Love God'
'Purify Your'
'Enrique'
'Gift Of God'
'Religion'
'Chosen Blood'
'Jesus Heals'
'Holy Flame'
'Twinflames'
'The Torah Code'
'Jesus Christ Of The Son'
'The One Worthy Of Almighty God'
'How Much Is The One Worthy Of Gematria?'
'I Am Haqqamshi Christ The King I Am The Alpha And'
'Christ Returns V Years Ahead Of Schedule'
'In Lord Jesus Christ Name Free Every One'
'I Have The Lord Jesus Christ'
'All Frequencies And Timelines Align'
'Word Of Christ'
'His Only Begotten Son Christ'
'The Yahya Spell All Ah Wh Ah'
'I Am In The Captain Of Our Salvation'
'The Creative Story Ever Told'
'Deep Reminders Of True Reality'
'King David Reincarnated Has Returned'
'Jesus Christ Of The Utterance'
'Jesus Christ His Teacher'
'An Je Hovih To Stay Back K J'
'Manifested Physical Representation Of Logos'
'Interplanetary Currency'
'I Am The Life Of The Valley'
'Thee Lord And Savior Aec'
'Angel Of Yahweh'
'He Is Immanuel To Yeshua'
'Jesus Family'
'The Lord And Savior Aec'
'The Voice Of Motoneuron'
'In A New Body'
'My New Name'
'Sealed Am'
'Sons Of God'
'The Source'
'Frequency'
'Convention'
'Birthday Code'
'How Much Is New World In Gematria?'
'New World'
'Ye And Yang'
'Yin And Yang'
'Tokyo'
'Being His Divine Teacher'
'Crucifixion Is Horrible Man'
'Gevurah Am'
'May Am Fifth'
'King Am May Fifth'
'The Promised Land'
'The Light'
'He Man'
'Of War'
'Gematria'
'Input'
'True Ape'
'Alex'
'Five'
'How Much Is Alex In Gematria?'
'The Aec'
'Cain'
'Aqos'
'Elleven'
'Flores'
'Easter'
'Sagiso'
'The Lord Aec'
'Say Love Aec'
'Triple Eights'
'The 13 Satanic Bloodlines'
'Shakti'
'Shaddai El Chai'
'Last Am May'
'Aqos May Five'
'Houston'
'King Aec May Five'
'The Lord Of God'
'Sunday'
'Saturday'
'Gate Of Rock'
'Fifty Five'
'Not Everyones Who Says To Me Lord Lord Will Enter The'
'Thee Lord And Savior Alex E Campain Fifth Nineteen Seventy Two At One Forty Am'
'Thee Lord Alex E Campain May Fifth Nineteen Seventy Two At One Forty Am'
'Has Thee Lord Alex E Campain May Fifth Nineteen Seventy Two At One Forty Am'
'Dat M C Born May Fifth Nineteen Seventy Two At'
'As Lord Savior Born May Fifth Nineteen Seventy Two At One Forty Am'
'Thee Savior Born May Fifth Nineteen Seventy Two At'
'Thee Savior Born May Fifth Nineteen Seventy Two At One Forty Am'
'Dat Savior Born A May Fifth Nineteen Seventy Two At One Forty Am'
'H Lord J Born May Fifth Nineteen Seventy Two At'
'Our Jesus C Born May Fifth Nineteen Seventy Two At'
'Lord C Yeshua Born May Fifth Nineteen Seventy Two At One Forty Am'
'Immaculate Birth May Five Nineteen Seventy Two At'
'Lord C Yeshua Birth May Fifth Nineteen Seventy Two At'
'Immaculate Birth May Five Nineteen Seventy Two At One Forty Am'
'Yeshua Christ Of Nazareth Our Lord And Savior Was Born On This Day'
'Born A Friday May Fifth Nineteen Seventy Two At One'
'The Lord Born A Friday May Fifth Nineteen Seventy Two At One Forty Am'
'I Jesus Born Friday May Fifth Nineteen Seventy Two At'
'Count The Number Of Letters In Your Name'
'You Cheated On Her She Will Cheat On You'
'Our Lord Savior Alexandro E Campain'
'Our Lord Savior Alexandro Campain'
'Christo Return As A Lion Fulfilled'
'Yah Mhe Can Do This Is It Just I'
'Jesus Christ The Conquering Lion Is Back'
'The Antichrist Is Return With Ai'
'Your Daddy Is Yahweh'
'You Are A Beautiful Flower Of Christ'
'You Are Absolutely One Of The Kind'
'If Yeshua Knew'
'The Four Corners Of The Yhwh'
'Thee Lord And Savior Alexandro Campain'
'The Full Armor Of God Protection'
'Jewish Month Of The Spirit'
'Is Heavenly Worth My Efforts'
'The Whimsical Periods Of Existence'
'I Am The Lies That They Want To Kill'
'Jesus Reincarnation Reborn'
'He Is My God Symbol Apocalypse'
'Holy Spirit Sanctifier'
'Ability To Change The World Stone Game'
'Jesus Is It Verrines Melaon Cadmon'
'Bring Alive Is Terrible Thanks A Lot God'
'Christ With White Hair And Sword'
'God God God God God God God God God God God God God God God'
'What Is Name Of The Soul Of Salvation'
'White Jesus'
'Thee Lord Savior Alexandro E Campain'
'Im Black And I Turn Water Into Dcil'
'Praye Me Wrong'
'Gematria Is God Je'
'See What Is Good For Je'
'Negro Yeshua Two Has Returned'
'Thee Hidden One Is Christ H'
'Four Horsemen Of The Apocalypse'
'Children Celebration Of Almighty God'
'Decode If He Holy Son Of Almighty God'
'The Divine Child Is The Chosen Son Of God'
'Thee Lord Alexandro E Campain'
'A God Jesus Christ Go Down'
'I Jesus Christ Will Go Down'
'Thee Lord And Savior Alexandro E Campain'
'Inverse Ondhas Rec'
'Oh Good God Jesus Lives So Be It'
'Thee Lord And Savior Alexandro Enrique Campain'
'Thee Lord And Savior Alexandro Enrique Palma'
'I Am The True Vine And My Father Is The Vine Dresser'
'The Holy Spirit The Final Call Before The Apocalypse'
'The Second Coming Of Jesus Are United'
'Thee Lord Savior Alexandro Campain'
'The Quantum Still Repentance'
'The Important Return Of The Lord'
'People Also Ask'
'Messianic Seamless Garment'
'I Amnot With You'
'Not Much Time Left To Choose Jesus'
'Selfish Reasons'
'Infinitely Serve On TheLord'
'The Numbers Of Your Name Meaning'
'The Son Of David Jesus Christ'
'Who Is Yeshua In The Flesh'
'Jesus The Christ The Lords Holy Code'
'I Am A God Je'
'Immanueljehosua'
'How Much Is Decode Our Souls'
'Decode Our Souls Belongs To Him'
'Our Lord And Savior Jesus Christ'
'Jesus Christ Was A Normal Man'
'Jesus Christ Protects Little Children'
'The Math Behind The Letters Of The Alphabet Encoded'
'Y O U Are The Only One True Who I Am'
'The Dragon That Will Come True'
'Jesus Didn T Write Come True'
'Jesus A Walk Come True'
'Holy Jesus Above And Kind'
'Holy Miracle Walking'
'Holy Holy Holy Is Lord God Almighty'
'Our Lord And Savior King The Morning Star'
'Our Lord And Savior King Theo Bright Morning Star'
'He Is Our Lord And Savior The Bright Morning Star'
'He Is Thee Lord And Savior King The Bright Morning'
'He Is Thee Lord And King The Morning Star'
'He Is Thee Lord And Savior King The Morning Star'
'The Queen Of The Five Sins Is The Son Of Man'
'The Lord And King The Bright Morning Star'
'Loved By God'
'How Much Is The Universe In Gematria?'
'The Divine Wrath Of YHWH'
'Lord God Almighty Straight Up Jesus'
'The Divine Name Of Almighty God'
'The King The Bright Morning Star'
'Universal Divine Law'
'Holy Trinity Of Planet Heaven H H H'
'Your Jesus Christ Is The Savior'
'Our Lord Savior Alex Campain'
'Our Lord Savior Alex Enrique Campain'
'God Is Talking To You Via Car License Plates'
'I Love Yahweh Elohim'
'All The Worlds A Stage And All The People Players On'
'Gematria Proves The Words Youall Choose'
'Catholicism Is A Percentage Of Jesus Teaching'
'Holy Spirit Of The Lord God Me I Love You'
'Jesus Christ Is Real Not A Myth'
'DREAMORGASMDEATHORDREAMORGASMDEATHOR'
'Yes Have Heard God Is Real Po'
'The Cross Of Jesus Christ'
'Yahweh The Living God'
'Simple Reasons Messiah Jesus'
'Get Lord Savior Alex Enrique Campain'
'He Is Saving The Whole Universe'
'The King Who Is To Be The Bright Morning Star'
'Jesus Christ Returned Last Year'
'Thee Lord Savior Alexander Le Campain'
'Lucifer The Kings Ruler Other'
'Who Is Lord Jesus Christ'
'Thee Lord Savior Alexander Campain'
'Our Lord Savior Alexander Campain'
'Thee Lord And Savior King Theo Bright Morning Star'
'The Lord And Savior King Theo Bright Morning Star'
'The Lord And Savior King Theo Morning Star'
'Lord And Savior King The Bright Morning Star'
'The Lord And Savior King Our Morning Star'
'Thee Lord And Savior King Our Bright Morning Star'
'The Star Of The Peace'
'He Is Our Lord And King The Morning Star'
'The Lord And King The Morning Star'
'Thee Lord And King The Morning Star'
'Christians With A New Body'
'IAm God Jesus Christ',
'I Am God Jesus Christ',
'Twin Flames Spirits',
'The Close To God',
'Jesus Anointing',
'Hidden Truth Is Revealed',
'Jesus Christ Grace',
'Jacob Crystal Dream',
'The Effects Of Deciphering Gematria',
'Divine Intervention',
'The Holy Spirit In The Flesh',
'New Name Of Messiah God',
'Alejandro Enrique Campain Born The Fifth Of May',
'Homosexuality Is Embraced By The Tree Yshueeh',
'The Meaning Of Life As Found Through The Gematria',
'The Tree Of Life And Tree Of Knowledge Are The T W I',
'Jesus Christ The Way Truth And The Light Life',
'I Am The Way The Truth And Life Mdm Lion',
'Alejandro Enrique Palma Campain Born The Fifth Of',
'God Send Your Second Coming Before It Is Too Late',
'Jerusalem Living Sacrifice',
'Alex Enrique Palma Campain Born The Fifth Of May',
'The Extrum Cost Of The Jewish Order',
'Alex Enrique Campain Born The Fifth Of May',
'Yeshua My Soul Belongs To You Am',
'Jesus Christ God Is A Human And His Name Is',
'Beast Worthy To Open The Book',
'The Fifth Of May',
'Christmas Eve',
'Yeshua Ha Mashiac',
'Sacred Geometry',
'Jesus Christo',
'Jesus Reappears',
'God In Human Form',
'Gods Secret Plan',
'The Cia Knows Alejandro Campain Gematria Stats And They Are Scared',
'Jesus Loves The Little Children Of The World',
'The Cia Knows Alex Campain Gematria Stats And They Are Scared',
'Our Savior And King Alex Enrique Palma Campain',
'Iesus Hominum Salvator',
'Our Lord And Savior Alex Campain',
'Jesus Rey Christ Lst',
'Alejandro Campain Born The Fifth Of May',
'The Mayor Jesus Christ Of Peace',
'I Am Avenging The Voice Of God',
'Gods Code Translation Perfected Gene',
'Jesus Christ Gods Son',
'Jesus Christ Gods Son Savior',
'The Most Godly Woman Ever Born',
'I Am The Way And The Truth And The Life',
'Holy Gene Sophia Of The Trinity',
'The Christ Aec',
'What Is The Meaning Of Jesus And Alex Campain',
'Christ Aec',
'Infinite',
'The Lamb Of God',
'Aec May Fifth',
'I Am Jesus',
'God Particle',
'The God Particle',
'Peaceful Warriors',
'Alpha God Particle',
'The Hidden',
'All In One',
'What Is The Meaning Of The Gift',
'Prayer De Guadalupe',
'Mary And Christ And Abba Yhwh We Rock Backs',
'Alejandro E Campain Born The Fifth Of May',
'Alexander E Campain Born The Fifth Of May',
'I Am Coming For You At The Rapture',
'Jesus Is Coming To Take You Home',
'The Prophet Warned',
'The True Jesus Christ Repentance',
'Yeshua Wanting It',
'What Is The Meaning Of May Fifth Nineteen Seventy Two',
'Alexander Enrique Campain Born The Fifth Of May',
'The Self Esteem Yahweh',
'The Gematria Of Awakening Consciousness',
'Yeshua Christ Goes Savior',
'Jesus Christ Is A Sinner',
'The Anointed Twins',
'Yahweh Yehovah Father Of Truth',
'Decode The Spirit Soul Birth Are',
'Alexander Campain Born The Fifth Of May',
'Decode The Cia Is Scared Of Jesus Christ',
'Angel Of Jehovah',
'The Divine Alignment Gematria',
'Jackie On The Cross',
'Our Groove Has A Message For You',
'Manifestation Of Love And Light',
'Yeshua I Know That You Returned',
'The Lord Savior Christ Of Jesus',
'Lexus Is A Jesus',
'Jesus Christ God Is A Sinner And His Name Is',
'Jesus Gematria Decipher',
'Alex E Campain Born The Fifth Of May',
'A Who Are The Two Witnesses',
'The Host Of The Living God',
'Yahweh',
'The Ancient Has Awakened',
'Jesus Every Cross Doing Horse',
'Holy Grail Reincarnation Of God',
'The Triple Eight Green Is Sacred',
'Almighty Lord Jesus Christ',
'The Lord And Savior King Our Bright Morning Star',
'Jewish Gematria Calculator',
'Are Jesus Of Nazareth Living Son Of See Of God',
'Am Son Of I Jesus Of Nazareth Living Son Of God',
'The Five Of Lord Jesus Christ',
'Jesus Christ The Savior',
'The Lord Savior Alexandro E Palma Campain',
'Jesus Christ Is The Only Way Truth And Life',
'Almighty Jesus Is Eternal In Eternal Hall',
'The Lord Savior Alexander Enrique Palma Campain',
'Our Lord Savior Alexandro Enrique Campain',
'Our Lord Savior Alexandro Enrique Palma Campain',
'Thee Lord Savior Alexandro E Campain',
'Thee Lord Savior Alexandro Enrique Palma Campain',
'Thee Lord Savior Alexandro Campain',
'Thee Lord Savior Alexandro Enrique Campain',
'Jesus Christ Was Born The Fifth Of May',
'Jesus Christ From The Fifth Of May',
'Almighty God Of The Great Tribulation',
'Decode Jesus Christ Was Born May Fifth',
'Decode Jesus Christ May Fifth',
'I Am The Second Coming Of Christ',
'John Twelve Forty Four',
'John One Two Four Four',
'You Are The Begotten Son',
'Psalms Seventy Three Jesus Christ The Return Of',
'Psalm Twenty Three Psalm Jesus Christ The Return Of David',
'Our Lord E Campain Born May Fifth Nineteen',
'Our Lord Alex Campain Born May Fifth Nineteen',
'Jesus Christ Was Born The Fifth Of May Nineteen Seventy',
'Yeshua Christ Was Born The Fifth Of May Nineteen',
'Yeshua Christ Was Born May Nineteen Seventy Two At One Forty Am',
'Thee Lord Alexandro E Campain Born M',
'Yeshua Christ Was Born May Nineteen',
'Yeshua Christ Born The Fifth Of May Nineteen',
'Our Savior Alex Campain Born May Fifth Nineteen Seventy Two One Forty Am',
'Our Savior Alex Enrique Palma Campain May Fifth Nineteen Seventy Two At One Forty Am',
'Jesus Christ Our Lord Was Born The Fifth Of May Nineteen Seventy Two At One Forty Am',
'Jesus Was Born The Fifth Of May Nineteen Seventy Two',
'Yeshua Real Was Born The Fifth Of May Nineteen Seventy Two At One Forty Am',
'John Twelve Four Four',
'June Twelve Forty Four',
'Our Lord Alexandro E Campain Born Fifth Nineteen',
'Jesus Cried Out With A Loud Voice Father Into Your Hands I Commit My Spirit',
'Find Out When And Where The Messiah Was Born Is Born In The Future Past Or Present Me',
'Our Lord Alexandro E Campain Born May Fifth Nineteen Seventy Two At One Forty Am',
'Calculate Gematria',
'Her Ac May',
'Antichrist',
'Am May',
'Hes King Ac',
'The Divine Twin Flame',
'The Tetragrammaton',
'He Is Our Alex E Campain',
'John Three Sixteen',
'For God So Loved The World That He Gave His One And Only Son That Whoever Believes In',
'Hola Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth',
'How Much Is John Three Sixteen In Gematria?',
'Christ Yeshua And Mighty Jesus Comes',
'The Son Of Christ And Number Struggles',
'You Are Of This World I Am Not Of This World',
'El Es Nuestro Savior Alex Enrique Palma Campain',
'Yeshua Ha Yhwh',
'How Much Is Yeshua Ha Yhwh In Gematria? Meaning Yeshua Is Ha Yhwh People',
'I Am Responsible For Bringing Heaven On Earth',
'He Is Beginning To Look A Lot Like Christmas',
'El Es Nuestro Savior Alex E Campain',
'El Es Nuestro Salvador Alex Enrique Palma Campain',
'El Es Nuestro Savior Alex Campain',
'El Es Nuestro Alex E Campain',
'Just Top Blend S',
'Porque De Tal Manera Amó Dios Al Mundo, Que Ha Dado A Su Hijo Unigénito, Para Que Todo',
'El Es Nuestro Savior Y El Rey, Alexandro Enrique Palma Campain, Nacido El Viernes Cinco De',
'Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth Nineteen',
'He Is Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth',
'He Is Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth Nineteen',
'He Is The Lord And Savior Our King Alexander Enrique Palma Campain Born Friday May Fifth Nineteen',
'Our Lord And Savior The King Alexander Enrique Palma Campain Born Friday May Fifth Nineteen Seventy Two At One Forty Am',
'Our Lord And Savior Alex Enrique Palma Campain Born Friday May Fifth Nineteen Seventy Two',
'The Blood Lines',
'The Blood Line',
'Da Vinci Secret',
'He Is The Lord Aec',
'Imparity',
'The Divine Child',
'Alex Campain',
'No Coincidence',
'The Healers',
'The Rh Negatives',
'Catholic Church',
'Mr Je Sus',
'Flower Of Life',
'God Is The Force',
'God Is With Me',
'Roman Catholic',
'The Living God',
'The God',
'He Is Lord Aec',
'I Know Coded Language',
'Dot',
'Lucifer',
'The King Is Coming',
'The Final Battle',
'I Am King Is Coming',
'The Lion King',
'I B B M',
'Son Of Satan',
'What Is The Meaning Of Alex Enrique Campain',
'Judgment Day',
'Lord Of Love',
'In Shape Of A Body',
'Finalis Ludi',
'Rewards System',
'The Ghost Aec',
'Miracles Happen',
'Lord God Is Here',
'Fifth Dimension',
'The Lost One',
'Give God',
'Blessed Is God',
'Blessed By God',
'House Of Bread',
'Periodic Table',
'Tree Of Life',
'Gods Birth Code',
'The King Is Back',
'Star Of David',
'Divine Light',
'King Jesus Bible',
'Middle Path',
'The Gods Code',
'The Biblical Messiah',
'The Gods Code Of God',
'On The Face Of The Earth Je',
'Your Jesus Christ',
'You Are Jesus Christ',
'Lord Alex Campain May Fifth',
'Alex Campain May Fifth',
'Quantum Physics',
'Simulative Theory',
'The Society Of Jesus',
'The Unknower Of The King',
'Jesus The Messiah Has Returned',
'Psalm Twenty Three',
'The Lord Is My Shepherd I Shall Not Want',
'I Am Honored Christ The King I Am The Alpha And',
'In The Beginning Was The Word And The Word Was With God And The Word Was God',
'Jesus Christ King Of Kings And Lord Of Lords',
'In The Beginning God Created The Heavens And The Earth',
'The Bright And Morning Star',
'The Image Of The Invisible God',
'Jesús Descendit De La Cruz A Las Cinco Mil',
'Jesús Oloroso De La Muerte',
'As Oor Dan Bor Hec May Sec MKL',
'Rey Jesus, El Hijo Del Adiosista Que Pueden',
'Soy Dios Tengo El Mismo Poder Que Jesus Y Tu May',
'You God Is Sitting On His Throne That You May Return To My Sacred Comfort',
'Christian Substance',
'The Only One God',
'Holy Holy Shekinah',
'The Second Coming Of Jesus Christ Left Sofiablo',
'Gods Holy Shekinah',
'Your True Father',
'Lord Of Story',
'Lucifer Gates',
'Gods Perfect Number',
'Divine',
'The Most High God In The Flesh',
'The First And The Last',
'Moon Fith Yod He',
'Jesus',
'The Aleph Tau',
'Jesus Kyrios',
'Alex Campain Birth',
'Gematria Org',
'How Much Is Jesus Kyrios In Gmatria? What Is The Meaning Of',
'Hidden History',
'Let There Be Light',
'How Much Is Let There Be Light In Gematria?',
'Humble And Meek',
'The Fold Crosses',
'Yeshua Christ',
'God The Father',
'Radi Hackanah',
'The Greatest Teacher',
'Intercession Of God',
'The Christ Force',
'Twin Flames Unite',
'Bloodline Of Yeshua',
'Yeshua Lod Statistic',
'One Source Plant And Seed And Everything In Between',
'The Greatest Story Ever Told',
'The Revelation Of Jesus Christ',
'The Fairy Flavors Hearts Love Wine',
'Something Good Is Going To Happen',
'Ah Is Flower See Jesus',
'Alex Enrique Campain',
'Thirteen Is Gods Number',
'Alex Enrique Campain Birth',
'Satan Code',
'Twelve Tribes Of Israel',
'Permit Blood Of Christ',
'I Am Colour',
'The Kingdom Of Heaven',
'The Energy Source',
'What Is The Meaning Of Alex Enrique Palma Campain May Fifth Nineteen Seventy Two at One forty AM',
'The Mouth Of Apocalypse',
'I Am The Lily Of The Valley',
'The Birth Information Of Jesus Christ',
'The Lord And Shepherd',
'Yeshua Will You Send Me A Message',
'The King And Savior',
'The Anti War Jesus',
'The Most High Is The Sun At Rize',
'I Am Most Powerful Angel On Earth',
'I Love Jesus Christ Yall Better Worship',
'Yeshua Are U Really Your Bride',
'Come With Sweet',
'Alex Enrique Campain Born May Five',
'The Second Coming Of Jesus',
'Jehovah Yireh Sabbath The Renewerge',
'The Blessing Of Abraham Comes Upon You',
'The Whole Duty Of God',
'The Resurrection Of Jesus Christ',
'Canonical Gospels',
'The King And I AMIAM',
'The Canonical Gospels',
'The Four Canonical Gospels',
'Our Lord And Savior Alex',
'Our Lord And Christ Aec',
'King Of New Jerusalem',
'The Holy Trinity',
'Prophets Of Yahweh',
'Golden Proportion Of God',
'Da Vinci Code',
'Hidden From Your Eyes',
'Who Is The Son Of God',
'Our Lord And Goliath',
'Twenty Six',
'Thoth Fif Ty Three',
'Thee Lord Christ Aec',
'Lord Christ Aec',
'The God Of Heaven',
'Jewish Indeed',
'Blessing Of God',
'God Came To Earth',
'Priesthood',
'John Fifteen Three',
'In Jesus Christo I Pray Every Child',
'May Fifth One Nine Seven Two One Forty',
'The Lamb Who Is Worthy To Have The Book',
'The Book Of Genesis Chapter One Verse Three',
'The Tree Of Life Also In The Midst Of The Garden',
'Jehovah Is Satan And His Father Is',
'Mid Brain Two Four Sixes',
'The Lion Of Juda Reveals Gods Spiritu Book',
'The Heat Of God Answered Through Gematria',
'May Five One Nine Seven Two One Forty',
'The Lamb Of Light Is Back Again Through Love',
'Birth Code Information Of Jesus Christ',
'Birth Information Of Yeshua Christ',
'Birth Information Of Jesus Christ',
'Spirit In The Sky',
'Remember Your Oath',
'Lord Quesalcoatl',
'The Autumn God',
'Is Faithful To Christ',
'God Is Showing You',
'The Son Of Man Revealed',
'Only Begotten Son',
'Son Of David',
'Our Lord Alex Campain',
'Holy Place Sanctuary',
'Moon Shila',
'Decode Messiah Christ',
'Divine Presence',
'Lord Alex Campain May',
'Holy Is My Godly Son',
'On Earth As It Is In Heaven',
'Alex Campain Is God In Human Form',
'Our Lord And Savior Alex E Campain',
'The Name And Number Of Horse And Numbers',
'How Much Is Alex Campain In Human Form In Gematria? What',
'The Garden Of Jesus Christ',
'Jesus Christ Is The Lion Of God',
'Our Lord Of The Living Waters',
'Tony Witnesses',
'Alex E Campain Is God In Human Form',
'I Am The King And The Truth And Life',
'He Had God He Was By Himself',
'Tag Identifies AECOE Revealed',
'Jesus Christ Gods Son Risen',
'Christ Returns With A New Name',
'A Yahwehs Salvation',
'Alex Campain Is With His Spiritu Partn',
'Jesus Christ Is The Way',
'Alex Enrique Campain In Human Form',
'The Son Of Christ God Number Struggles',
'Alex Enrique Palma Campain In Human Form',
'Birth Of The New World Order',
'Reincarnation Of The True God',
'The Holy Unknown Name Of God',
'The Eternal Voice Of The People',
'Jesus Is Left',
'The Man King',
'The Messiah I Am The Chosen One',
'I Am God In Human Form',
'Alex Enrique Campain Is God In Human Form',
'Yeshua Hamashiach',
'I Am The Worlds Most Powerul Telepath',
'Jesus Unconditionally Christ',
'I Am Who I Am Alexandro E Campain Is Jesus Christ',
'I Am Who I Am Alexander E Campain Is Jesus Christ',
'I Am Who I Am Alejandro E Campain Is Jesus Christ',
'The Most Powerful People In The World',
'I Am That I Am Alexandro E Campain',
'Jesus Christos Theos Soter',
'Resurrection Of The Christ Reason Of Kings And Kings',
'The Truth The Whole Truth And The Holy Truth',
'I Am He That Is Holy He That Is True He That Hath The Key',
'Jesus The One May To Come',
'I Am Who IAm Alex Campain Is Jesus Christ',
'Hi Im Yeshua Alexandro Campain Is Jesus Christ',
'Activate Holy Yahwehs Silver Fire',
'My Mission Is The Actual Jesus Christ The Lord',
'The Primus State Gliding And The Aquarian Rule',
'The Piscean Dark Gliding And The Aquarian Rule',
'I Am Who Am Alexo E Campain Is Jesus Christ',
'I Am Who Am Alex E Campain Is Jesus Christ',
'The Father The Son And The Holy Spirit',
'Two Horns Of God Am I Am Yeshua Jesus See A',
'The Father The Son And Holy Spirit',
'The Numbers The Numbers',
'One Hundred Forty Four Thousand',
'Gematria Is The Path Of Gods Message From God',
'Ahasis Jesus Christ',
'Moments In God And Awareness Is Lucifer',
'Sacred Texts Nobody Will Touch',
'God Chose You No Coincidence',
'Father Son And Holy Spirit',
'Mighty God God Daybrc',
'Pleasant Sequence I Murdered',
'I Know Is Gods Number',
'Purest Blood Of Christ',
'Gods Power',
'Foundation Of The World',
'The Holy Son Alex Campain',
'I Divinely God Jesus Name',
'Jesus From The World Je A Dc Dc',
'The Rebirth Of Motonorcy',
'There Is No God Like You',
'I H S Christ Jesus',
'The Incarnation Of Yeshua',
'This Holy Son Alex Campain',
'The Creators Son',
'How Much Is The Creators Son In Gematria? What Is The Meaning',
'El Es Nuestro Savior Y El Salvador Jesucristo',
'El Es Nuestro Savior Jesucristo',
'Nuestro Savior Y Salvador Jesucristo',
'Bobs Original Plus Was From Leon And Albrechto Oe',
'Bobs Original Plus',
'They Have Already Murdered You I Have Come Lol',
'Five Point Nine She Cooking Up The Universe',
'Jesus Judges The Living And The Dead',
'Alex Enrique Campain Is God Yhwh In Human Form',
'Gematria What Is The Next Important Thing',
'The Son Of God Is Amongst Us The Light Is Here',
'The Big Deception Is That Jesus Christ Is Lucifer And',
'Playerlia Chapter Twenty Five Verse On',
'Alex E Campain Is God Yhwh In Human Form',
'Yahweh The Father Of Yeshua',
'A Servant Of Yahweh',
'The Holy Spirit Mother God Sebastian',
'Alex Campain Is God Yhwh In Heaven Form',
'I Am The Second Coming Of Jesus Christ',
'Encode The Unknown Goddess Is Gematria',
'The A Qoeem Of Zeme',
'Thy Kingdom Come',
'The Holy Ghost',
'His Name Is Jesus',
'Jehovah Three Three Three',
'Zero One Two Three Five Eight Thirteen Twenty',
'The Most High God In The Rock',
'Allah Allah Allah Allah Allah Allah Allah',
'The Second Coming Of The Lord Jesus Christ',
'I Am Who I Am Alejandro Campain Is Jesus Christ',
'I Jesus Said I Am The Resurrection And The Life',
'Remember Your Oath Remember The Mission',
'Merry Christmas And A Happy New Year',
'Holy Wisdom',
'Faithful Witness',
'Infinity Symbol',
'Its Going To Be Biblical',
'The New Testament',
'The Hidden Key Code Of God',
'Holy Inpolution Of God Codes',
'The Living Word Of God',
'Seven Spirits',
'Jesus The Son',
'Holy Alex Campain',
'Jesus H Christ',
'Yhwh Alex E Campain',
'Shado The Messiah',
'The Word Of The Lord',
'I Reincarnated On The Third Day',
'What Is The Correct Model Of The World',
'The Messiah Past Present And Future',
'The Difference Between Actuality And Idea',
'The Royal Frequency Is Love',
'Am Jesus Of Nazareth Living Son Of God',
'Install How To Unique This Evil Realm',
'Decode Source Of The Horrible Name Of My Bible',
'All His Worth Is Belief Current And Truth',
'The Denial Reason Of All King David Reborn',
'The Gospel Truth Of All King David Reborn',
'The Return Of The Lord And Lady Christ',
'Decode The Gospel Truth Of Mary Magdalene',
'Decode Wrath Of God And The Hourly Curse',
'Decode The Cia Is Fearful Of The Sacred Christ',
'Value Of God Without Friends Gcl Gue',
'Any Day Now God Jesus',
'Jesus Only In The Litergy House',
'The Freemason World Order',
'Jesus',
    'Jesus A Listen ,Son Be Wise KG JC',
    'Jesus Christ Incarnated Into Alex Campain',
    'Jesus Christ Messiah',
    'Jesus Christ Reincarnated to Alex Campain',
    'Jesus Christ Solar Flash',
    'Jesus Christ The Song Of David',
    'Jesus Christ The Way The Truth And The Light',
    'Jesus Christ is Alejandro ENRIQUE Campain',
    'Jesus Christ is Alexander Enrique Campain',
    'Jesus Christ is Alive Today',
    'Jesus Cristo',
    'Jesus Immaculate Conception Of A Virgin Mary',
    'Jesus Jesus Jesus',
    'Jesus Just Think For Yourself',
    'Jesus King Of The Jews',
    'Jesus Our Redeemer',
    'Jesus Prays',
    'Jesus Raised from the dead',
    'Jesus Returns',
    'Jesus Teaches Love',
    'Jesus in the Flesh',
    'Jesus is Here',
    'Jesus is Necessary and Sufficient',
    'Jesus is coming to save his people',
    'Jesus is our Holy Breath',
    'Jesus of Nazareth',
    'Jesus prophecy',
    'Judgement Is Coming',
    'King Of All Kings AEC May Fifth',
    'King Of Kings Lords Of Lord',
    'King Yeshua Heavenly Father',
    'Know My Truth',
    'Lafler Day Saints',
    'Laws Of Mathematics',
    'Leb First Born Son',
    'Lift up Yahweh',
    'Living Lord',
    'Living Lord God Jesus Messiah',
    'Lord Alejandro Enrique Campain',
    'Lord Alex Campain',
    'Lord Alex E. Campain',
    'Lord Christ',
    'Lord God is Here, Lord God is Here, Lord God is Here, Lord God is Here',
    'Lord YHWH a Messiah',
    'Lord Yeshua The Lights of The World',
    'Los Angeles California',
    'Love',
    'Love Frequency Jesus Messiah',
    'Love Love Love Love Love',
    'Manifestation Of God',
    'Manifestation of Alex Enrique Palma Campain May Fifth',
    'May Fifth',
    'May Five MCMLXXII',
    'May Five Two Eight',
    'May Five nineteen seven two',
    'Merry Christmas',
    'Message from God To Alex Enrique Campain',    'Messiah',
    'Messiah Birthday Code',
    'Messiah God May Fifth',
    'Messianic',
    'Messianic Israel',
    'Miraculous Birth',
    'Moshiach Saviour G.',
    'Mr Alex Campain',
    'My Divine Love',
    'My Mission On Earth',
    'My Name Before I came Here',
    'My Son Is The King',
    'Name is Alejandro Enrique Campain',
    'Name is Alejandro Enrique Palma Campain',
    'Needs Verification',
    'New Jerusalem',
    'One Hundred and Forty To thousand',
    'One hundred forty four thousand',
    'Only God Exists',
    'Our King Christ The Moshiach A King Reborn On May Fifth',
    'Our Savior Alex Enrique Campain',
    'Our Yahweh Thee God',
    'Perfection Of Harmony',
    'Pleiadians Of Christ',
    'Pontius Pilate Crucified Alexander Enrique Palma Campain',
    'President Of The United States',
    'Project your heavens heart on earth',
    'Promised Gift Of God',
    'Proof of the past',
    'Reincarnated into Alex Enrique Palma Campain',
    'Reincarnation Of God',
    'Reincarnation of Jesus Christ',
    'Reincarnation of Jesus Christ IAM Back',
    'Reincarnation of Jesus Christ The Lord',
    'Resurrection',
    'Return Of Christ',
    'Return Of Zeus',
    'Returns on Earth',
    'Revelation Of Jesus Christ',
    'Revelation of word',
    'Revelation one Three one eight',
    'Rise From The Ashes',
    'Save Earth, Save The Children Stop War and Stop Greed',
    'Second Coming Of Jesus Christ',
    'Second Corinthians Four',
    'See IAm The Messiah Alpha And Omega First And Last Beginning And End',
    'Seven Spirits Of Chr6',
    'Seven two two zero eight seven',
    'Seventh Day Creation',
    'Shroud Of The Lord',
    'Shroud Of Turin',
    'Six hundred and sixty six code',
    'Six pointed Star Of David',
    'Son Of David C. Moshiach',
    'Son Of Yahweh',
    'Source Of Souls',
    'Spring Equinox',
    'Story Of My Life',
    'Synagogue Of YHVH',
    'Synchronicity',
    'Teaching The Wisdom JC',
    'Tell me who is Alex Campain',
    'Tell me who is Alex E Campain',
    'The AEC Of The Lord Jesus Christ',
    'The Age Of Aquarius',
    'The Best Secrets Of Gematria Revealed',
    'The Biblical Son Of God',
    'The Birth Of Christ',
    'The Birth Of Jesus C.',
    'The Birth Of Yeshua Christ Our Savior',
    'The Book Of Revelation',
    'The Bride Of Christ One like unto The Son Of Man',
    'The Bright Morning Star',
    'The Christ proof',
    'The Christianity',
    'The Crown Of Thorns',
    'The Crucified Christ',
    'The Day Jesus Arrived',
    'The Dialogue Of The Savior',
    'The Divine bloodline',
    'The Door Between the imagined and real opens soon',
    'The Dreadful Judge Is AEC',
    'The Essence Of YHWH',
    'The Etheric Field is The Unified field Of Consciousness',
    'The Five wounds of Jesus Christ',
    'The Geometry Of God',
    'The Geometry Of The Universe',
    'The God Given Name Angel',
    'The Holy Great One',
    'The Holy Lord Alex Enrique Campain',
    'The Holy Son Allah GD.',
    'The Holy Son Of El AEC',
    'The Holy Son Of Elah',
    'The Holy Son Of HAEL',
    'The Holy Son of God',
    'The Holy Song Of YA',
    'The Holy Spirit',
    'The Holy Spirit is The Spirit of Truth',
    'The Holy Sun Of God',
    'The Imminent Return Of Venus',
    'The Jewish G. Messiah',
    'The Key To Unlock Reality',
    'The King',
    'The King Christ Our Moshiach A King Reborn On May Fifth',
    'The King of the Jews',
    'The Knowledge Of Kabbalah',
    'The Lamb Is Pissed Off',
    'The Last supper',
    'The Light Bearer',
    'The Lion Of The Tribe Of Judah In My Heart',
    'The Lord Alex E Campain',
    'The Lord Alex Enrique Campain',
    'The Lord Identity',
    'The Lord Jesus Christ',
    'The Lord Returns',
    'The Lord The God Of Heaven And The God Of The Earth',
    'The Lord Will Guide My Steps',
    'The Lord in The Flesh',
    'The Magnificents of Three Six and Nine',
    'The Manifestation Of Jesus Christ',
    'The Master Yeshua',
    'The Messiah, The Christ, The Holy Spirit, The Son of God and The Son of The Living God',
    'The Morning Star',
    'The Mother Of Jesus Christ',
    'The New Christ Is an Aquarius',
    'The New Testament',
    'The Olive Harvest',
    'The Only One Who can Save The Earth',
    'The Prophecy Of The Child',
    'The Prophecy of Jesus Christ',
    'The Real Jesus Christ',
    'The Reinccarnated Buddha',
    'The Reincarnation Of Yeshua Christ',
    'The Return Glory Of Jesus Christ King Of Israel',
    'The Return Of Christ as The Lion',
    'The Returned Of Christ A Lord',
    'The Rose of Sharon',
    'The Salvation Of God',
    'The Savior Christ Alex Campain',
    'The Savior Jesus Christ The Lord',
    'The Saviour with white hair is',
    'The Second Coming Of Prometheus',
    'The Seven Seals In The Book of Revelation Are',
    'The Seven Spirits Of God',
    'The Singularity',
    'The Son of God born of a virgin',
    'The Son of God is amongst us the light is here',
    'The Son of God reincarnated',
    'The Son of Man',
    'The Tetragrammaton',
    'The Time Of Justice',
    'The True Messenger Of The God',
    'The Twenty Six Letters Of The English Alphabet',
    'The Two Olive Trees',
    'The YHWH A Holy Bible',
    'The Yeshu Christ',
    'The bible reveals itself to an open mind the Lord',
    'The birth of Yeshua our savior',
    'The decrypted code knows how to code',
    'He is the son of God',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'The feast of the immaculate Conception',
    'The five wounds of Christ',
    'The lamb who is worthy to open the book',
    'The mathematical formula of existence',
    'Thirty Three',
    'The root of David revealed through Gematria',
    'The second coming',
    'The second coming Jesus has Arrived',
    'The second coming of Jesus Christ will be hated',
    'The sign given of the prophet Jonas',
    'The true son of The Yahweh a living God',
    'The ultimate Lord Jesus',
    'The voice jesus is coming all peoples will answer to him at judgment',
    'The way the truth and the life',
    'Thee Holy God YHWH',
    'Thee Jewish Moshiach',
    'Thee King Son Of David',
    'Thee Lord God a Messiah',
    'Thee Lord Your Savior Alex E Campain',
    'This is the truth you are looking for',
    'This is your God',
    'Thou Art My Son',
    'Three Hundred and sixty-nine',
    'Thy Kingdom Come Thy Will Be Done One Earth as it is in Heaven in Jesus name Amen',
    'Time to wake up my people',
    'To Save The Children',
    'Translate God Word',
    'Tu Eres el Salvador',
    'Twin Souls Of God',
    'Two hundred and fifty six',
    'Ultimate Truth',
    'V -V, MCMLXXII',
    'Vicarius Christi',
    'What is the new Name?',
    'Where Are u Satan?',
    'Where is he now?',
    'Who Is A. MCXXVIII',
    'Who Is The A Creator',
    'Who Is The Bride Of Christ',
    'Who Jesus Christ was Reincarnated into',
    'Who is Alex Campain',
    'Who is Alex E Campain',
    'Who is Alex ENRIQUE Campain May Fifth',
    'Who is Alex Enrique Campain',
    'Who is Eleven Twenty Eight?',
    'Who is Jesus Christ?',
    'Who is King of the Aquarian age',
    'Who is The Savior?',
    'Who is able to save and to destroy',
    "Who's God The YHWH",
    "Who's The God YHWH",
    "Who's YHWH The God",
    'Whos Amung Us',
    'World Peace',
    'YHWH Good Shepherd',
    'YHWH Jesus Christ Alex Campain',
    'YHWH Messiah a Lord',
    'YHWH Returns AEC',
    'YHWH has Returns',
    'YOD HEH VAV HEH',
    'Yahushuwah Ha Mashiah',
    'Yahuwshah',
    'Yahve Is Alex Campain',
    'Yahweh Rules',
    'Yahweh confirms Alex E Campain is Jesus Christ',
    'Yahweh confirms Alex Enrique Palma Campain is Jesus Christ',
    'Yahweh returns with a Fleet of ships',
    'Yahweh, Yahweh, Yahweh, Yahweh, Yahweh, Yahweh',
    'Yehowah Salvation',
    'Yehowah is Male',
    'Yehowahs Hidden Son',
    'Yeshua Christ',
    'Yeshua Christ Incarnated Into Alex Campain',
    'Yeshua Christ Is AC',
    'Yeshua HA Meshiach Kin',
    'Yeshua Is On Earth',
    'Yeshua Jigsaw',
    'Yeshua Of Nazareth',
    'Yeshua reincarnated into Alejandro Campain',
    'Yeshua reincarnated into Alejandro Enrique Campain',
    'Yeshua reincarnated into Alex E Campain',
    'Yeshua return of The King',
    'Yod Heh Vov Heh',
    'You Are Eternally Married',
    'You Are The Son Of God',
    'You Are The Son Of Yahweh',
    'You Really Are The Second Coming Of Jesus Christ',
    "You are God's Only Messiah",
    'You are The Coder Of Your Reality',
    'You are The Light Of The World',
    'You are the second coming of Jesus Christ',
    'Your Messiah chosen by God',
    'Your Name Is Ahava',
    'Your The Moshiach',
    'Yowusa',
    'Yud Kei Wav Kei',
    'Yud Shin Waw Ayin',
    'Zero zero one two zero Vatican City',
    'aleph bet gimel dalet hey vav zayin chet',
    'four four four',
    'holy holy holy',
    'i am the second coming of jesus christ',
    'i am truly the christ and i was given a light throne and a new name',
    'king of the Jews',
    'my perfect love cast out fear',
    'revelation nineteen eleven',
    'reverse jesus died',
    'The Son Of God',
    'Alex Enrique Palma Campain',
    'Alex Enrique Palma Campain May Fifth Nineteen Seventy Two',
    'Jesus Christ The Son Of God',
    'Jesus Christ',
    'Morning Star',
    'Lamb Of God',
    'The Lamb Of God',
    'Iam The Way And The Truth And The Life',
    'No one comes to the Father except through me',
    'Yeshua Christ Second Coming',
    'Jesus Christ Second Coming May Fifth',
    'Yeshua Christ Second Coming May Fifth',
    'Moshiach',
    'Mashiach',
    'Mesias',
    'Yeshua Christ The Secong Coming May Five',
    'Jesus Christ The Second Coming May Five',
    'Alex Campain is God YHWH',
    'Alex Campain is God on Earth',
    'Alex Enrique Campain is The Son Of God',
    'The Bread Of Life',
    'Bread Of Life',
    'Elohim',
    'Jireh',
    'Rapha',
    'Rafa',
    'El Shaddai',
    'YHWH',
    'Yahweh',
    'jesucristo',
    'Dios',
    'Deu',
    'Dios Todo Poderoso',
    'May Five',
    'May Fifth Nineteen Seventy Two',
    'May Five Nineteen Seventy Two',
    'Jesus Christ King Of Kings Lord Of Lords',
    'Come to me all who are weary and burden so that I may heal you',
    'God in the Flesh',
    'Shiloh',
    'The Branch',
    'Alex Campain is the Son Of Man',
    'he is the Son Of ManThe God Entity',
    'King Yehoshua',
    'Lord of Lords',
    'Messiah Returns',
    'Davincicode',
    'Wife of Jesus',
    'The Finish Line',
    'The Month of May',
    'Its Doomsday',
    'True Messiah',
    'Lord Almighty Bible God',
    'Yhwh Messiah',
    'Yhwh Energy',
    'Stay Focused',
    'Christchurch',
    'Divine God',
    'Our Savior',
    'Spirit of God',
    'Revelation Chapter Six',
    'Lord Jesus Christ',
    'Jesus Messiah Gods Vengeance',
    'O Love Yhwh',
    'Jesus Is Real',
    'Glory To God',
    'I Am Yhwh God Moshiach',
    'El Shaddai Elohim Yhwh',
    'Yeshua Ha Moshiach Kin',
    'Art The Promised God',
    'El Es Jesus Cristo',
    'Jesus Christ Is I',
    'Messiah Birthdate Code',
    'know Yhwh Yahweh',
    'Know Yhwh Elohim',
    'Uv Uv Uv',
    'I Am Yhwh Saver',
    'I Moshiach Saviour',
    'What Is The New Name',
    'Allah Yahweh Savior',
    'He Is Our All The God',
    'Eliha Elihi Elohim Yhwh',
    'Yahweh Adios Yahweh',
    'Un Dios Adios Yhwh',
    'A Savior The Yhwh',
    'Welcome Thee Jesus',
    'Rey Messiah Jesus',
    'Nuestros Mesios Y Dios',
    'I Yhwh Moshiach A King',
    'I Yhwh Messiah King',
    'I Am Yhwh I Am That I Am',
    'Im The Son Of Yhwh',
    'Rapture Is Coming',
    'I Am Who I Am God Yahweh',
    'Nuestro Dios El Mesias',
    'Rey Mesias Jesus',
    'May Five Mcmxlxii',
    'I Am Son Of Thee Father',
    'Our Father Moshiach',
    'Federal Reserve',
    'November Fifth Twenty Twenty Seven',
    'A True And Verified Prophet Of God The Seal Of God',
    'Six Six Six Reverse English Sumerian',
    'Hawah Elohim',
    'November Fifth',
    'God Almighty Sword',
    'The End Is Now',
    'Heaven On Earth',
    'Great Awakening',
    'Nuestro Padre Moshiach',
    'Campain Del Mesias Alex El 5 De Mayo',
    'Jesucristo Resucitado',
    'The Lion Of The Tribe Of Judah',
    'Moshiach Alex Campain May Five',
    'The Book Of Genesis Chapter One Verse One',
    'Moshhiach Alex Campain May Fifth',
    'Five One Nine Seven months until May 2027?',
    'Five One Nine Seven',
    'Born On This Day A N D H E Is K I N G O F N A T I O N S Saving The Meek',
    'Jesus Enseña El Amor',
    'Amor Aec',
    'El El',
    'Cinco De Mayo',
    'Immanuel',
    'Plan De Los Dioses',
    'Un Amor',
    'Sacred Hebrew Alphabet',
    'My Birthday Is May Fifth Nineteen Seventy Two',
    'El Sagrado Alfabeto Hebreo',
    'I Am Yahshua The Moshiach King of Kings and Lord of Lords',
    'If You Only Know The Meaning Of Three Six Six Nine',
    'Fifty Seven',
    'The Garden Of Eden',
    'The Angel Of Death',
    'A Yesus',
    'Oh God',
    'Hes Back',
    'God Name Amen Ra',
    'Iam nothing',
    'End Game',
    'Lord',
    'I Am God',
    'The King Is Back',
    'Aleph Nun Yod',
    'The Reflection Of Self Is S',
    'Symmetrical',
    'Son Of Jehovah',
    'God Victory',
    'God Of Gematria Calculator',
    'Jehovah Is Alex Campain',
    'A Rebirth Of Yeshua The Christ In Alex E Campain',
    'Yeshua The Christ Reincarnated Alex Campain',
    'Christ Reincarnated Alex Campain',
    'Aec Yeshua Christ Has Returned To Earth',
    'He Am Yeshua Christ Has Returned To Earth',
    'Am God Today We Are Sent To Earth',
    'Dad Head Aec',
    'The Planet Mars',
    'Encode Metatron',
    'Decode May Fourteenth',
    'Glory Of Love',
    'Easter Sunday',
    'My Frequency',
    'I Forgive You',
    'Decode Three Keys',
    'Abba',
    'Lieb',
    'Kabaala',
    'Aec May Five',
    'Revalations',
    'Mathematical Codes',
    'Truman Show',
    'Heart Over Mind',
    'I Am The Holy Spirit Of God',
    'Thirty Six',
    'A B C',
    'A E',
    'Big Head',
    'Dad Head',
    'Kabbal',
    'Previous Code',
    'Power Of Love',
    'Messenger Of God',
    'Identity Codes',
    'The Holy Keys',
    'Encoded Jesus',
    'Moshiachmoshiach',
    'Perfectly Balanced',
    'Restorative',
    'Two Five Six',
    'The Master Plan',
    'My Prophecy',
    'Word Code',
    'Financial Collapse',
    'Your Logic Code',
    'Save The World',
    'Third Horses',
    'Subzero Codes',
    'Blue Archive Codes',
    'Read Verified Codes',
    'A Man Of The People',
    'God Warned You',
    'Campaign Expert',
    'The Star Of David',
    'God Intervening',
    'Ancestors Of Our Past',
    'Lord Of Hosts The God Of',
    'Language Of Heaven',
    'Hidden Enery Codes',
    'Mother Goddess',
    'Campaign Window',
    'The Hypocrite',
    'Constant Codes',
    'You Are The One',
    'Identity Sir',
    'My Birthday Code',
    'Decode Jesus',
    'Ray Of The Sun',
    'The High Priest',
    'All Decrypted Code',
    'My Purification Is',
    'I Do Believe In Miracles',
    'A Bible Revalation',
    'Accumulations',
    'Your Number',
    'Coatedcodeofarmer',
    'Bridge Currency',
    'Seventy Five',
    'Interpret Code',
    'Smoker Messiah',
    'The Gift At The End',
    'The All Seeing Eye',
    'Son Eternal Death Is Coming',
    'A Measurement Of Time',
    'Decode Holy Bible Father',
    'Heal The World',
    'Divine Sophia',
    'David And Goliath',
    'God He Will Come',
    'Bible Gematria Code',
    'Daughter Of God',
    'Mother Earth',
    'The Alpha And Omega',
    'The Golden Key',
    'Gemini Messiah',
    'Who Are You',
    'Son Of The Illuminati',
    'Holy Orders',
    'The Holy Breath',
    'Abuelito Manona',
    'Yo Soy Tu Dios Jehova',
    'Jesus Is King',
    'Our Holy Lamb of God',
    'Is Identified As A Real God',
    'God Is Here In The Flesh',
    'La Estrella De La Manana El',
    'Ac Él Es El Verdadero Lucifer',
    'Ac He Is The True Lucifer',
    'Ac He Is The Real Lucifer',
    'El Verdadero Nombre De Lucifer',
    'Lucifers Real Name',
    'Lucifer He Is Real',
    'The Only God Jehova',
    'The Only God Yhwh',
    'The Only God Yahveh',
    'Salvador Mesías Un Rey',
    'Savior Mashiach A King',
    'I am Jehovah Yahweh God',
    'I am Jehovah God',
    'I am Jehovah Yahweh',
    'Superman Kripton',
    'Ac This Our Earth Our Universe',
    'He Comes With Judgment',
    'Im Your God Jehova',
    'Yo Soy Jehová Yahvé Dios',
    'The Only God Yhweh',
    'Answer Me My Father So That These People May Know Who You Are Then Christ Alex Enriquen Campain May Fifth Nineteen Seventy Two',
    'If The World Hates You Know That It Has Hated Me Before It Hated You King Mashiach Alex Enriquen Campain May Fifth Nineteen Seventy Two',
    'Alexander Enriquen Campain May Fifth Nineteen Seventy Two',
    'Our Saviour Alex Campain May Fifth Nineteen Seventy Two',
    'Jesus Is Only Here To Show The Light And Way For Alex Enriquen Campain May Fifth Nineteen Seventy Two',
    'Decode Yhwh God Elohim',
    'The Savior Mashiach',
    'The Root Of David Has Been Hidden From The People',
    'Our Mashiach The King Reborn On May Fifth',
    'Morningstar Jesus Christ',
    'Yeshua Christ Born In This Year',
    'This Is Jehovah',
    'Yes He Is Yeshua Christ',
    'Jesus Christ Is Mr Campain',
    'La Palabra Era Dios',
    'The Word Was God',
    'Dios Todavía Está Aquí',
    'Also Enrique Campain Jesus Of Nazareth Are The One',
    'Decode The Church Of Scientology Knows Who The',
    'God So Loved The World That He Gave His Only',
    'Evidence That Real Gods Are Smarter Than Their Worshiping Data',
    'Jesus Of Nazareth And Alex Enrique Campain Are One',
    'Salvador',
    'El Lado De Dios Yeshua',
    'Un Dios De Alta Autoridad',
    'Es El Espíritu Santo',
    'Solo Para Siempre',
    'Forever Alone',
    'Worded',
    'Activate God Code',
    'God In Numerology',
    'Apple Of My Eye',
    'Fifty Fifty',
    'Has The Holy Spirit',
    'The Lions Start',
    'A High Authority God',
    'The Side Of God Yeshua',
    'To See El Mesías',
    'Year The Mashiach',
    'Yhwh Cristo Cordero',
    'A Dios A Jesucristo',
    'Hijo De Dios Yhwh',
    'Es Jesucristo May',
    'Un Jehová Yhwh Elohim',
    'A Jehova Yhwh Dios',
    'Un Jehová Yhwh',
    'Jehovah Shalom',
    'The Lion Of Jesus Christ',
    'Jesus Resurrected',
    'One Eighty Eight',
    'Name Of The Lord',
    'The Biblical Messiah',
    'Seven Twenty Eight',
    'Your King Is Already Here',
    'Second Coming Of Christ',
    'El Dios Yhwh',
    'El Dios Yhwh Elohim',
    'What Is My Name',
    'Jesus Christ Is A Human Being Alive Now Us Today',
    'Decode Jesus Christ Is King Of Kings And Lord Of',
    'I Am Yeshua The Messiah King Of Kings And L',
    'Chulo Visita Perris Meets Jesus Reborn May Fifth',
    'In The Name Of The Father And Of The Son And Of The',
    'Pay Attention To The Holy Spirit Warning Signs',
    'Alex Enrique Campain T Jesus De Nazaret',
    'Reencarnación De Jesucristo El',
    'The Birth Of Jesus Of Nazareth',
    'The Birth Of Alex Enrique Campain',
    'The Birth Of Jesus C',
    'You Already Know The Truth At Age Five',
    'The Holy Soul Of Almighty God',
    'Jesus Christ Personified',
    'God In Spanish Is Dios',
    'Purifying The Earth',
    'An Alphamemetric Code Of',
    'Arrival Of The Lord God',
    'Fatherresurrected',
    'God The Holy Spirit',
    'Happy Birthday Mary',
    'The Matrix Is Real',
    'Jesus On The Cross',
    'Conceivable',
    'Cycle Of Rejuvenation',
    'Reincarnated Prophet',
    'The Meaning Of The Mess',
    'Jesus And Mary Had Child K',
    'New Heaven And New Earth',
    'How Much Is Your Dad Is In',
    'How Much Is Easter Day Codes In',
    'Mashiach Existence',
    'The Dimension Of Love',
    'Remember Who You Are',
    'Name Of My True Love',
    'Spiritual Awakening',
    'Decode Due God Fuse',
    'I Am The Son Of God',
    'JESESCHRISTUS YESCHUSCH',
    'The New Christ Who Revealed Himself',
    'The Same Numerical Value In English Gematria And',
    'Jesus Of Nazareth Reincarnated Jesus Enrique Campain',
    'Matthew Twenty Four',
    'Jesus Of Nazareth And Alex Enrique Campain Are The',
    'The Great Return Of Queen And King Sophia Yeshua',
    'The Misetela Town Of The Universe Five Twenty Eight',
    'Jesus Of Nazareth Alex Enrique Campain Are One',
    'Jesus Christ Was Begotten',
    'Decode Lord Lucifer Christ',
    'Instruction Of God',
    'Yeshua Is Me',
    'The Birth Of Alex Campain',
    'I Am The Lord Your God',
    'I Rest Body Yeschua',
    'Decode I Am Jesus Christ',
    'Jesus Of Nazareth Is The King',
    'Christs New America',
    'Ultimate Youth',
    'Here To The Throne',
    'Owns Salvation',
    'Gods Love',
    'Gods Voice',
    'You Call Me Teacher And Lord And You Are Right Because That Is What I Am',
    'He Is The Captain Of Our Salvation',
    'The Second Coming Of Jesus Christ',
    'Jesus Lord',
    'Vic Mundo',
    'Am Reborned Messiah',
    'Mashiach Christ Lord',
    'He Is The Christ Lord',
    'Our Christ Lord',
    'A Holy Christ A Lord',
    'Jesus Christ The Holy Son Of God',
    'The Secret Of Eternal Life Revealed',
    'Eleven Twenty Eight',
    'Love Love Love',
    'The King Of God',
    'Decode Lord Jesus',
    'Twenty Six',
    'The Messiah Has Returned',
    'Aleph Campain',
    'Aleph',
    'Nine',
    'Christ Christ Christ Christ Christ',
    'Re Reincarnation Jesus',
    'Alef',
    'Reincarnated Date The Fifth Of May Name Is Alex',
    'I Will Bring My Salvation To The Ends Of The Earth',
    'Hello Father Please Continue To Hold Your Head High So That We Are Praying For The Safety Of Your',
    'What If We Are Here To Save Jesus',
    'May Five The Reincarnation Of Jesus Christ',
    'Jesucristo Es Reencarnación En Alex Enrique Campain',
    'El Dios Jesus Reincarnate Into Alex Enrique',
    'Alex Enrique Campain Is Jesus Christ Savior',
    'Alex Campain Is Jesus Christ Our Lord',
    'The True King Of The Kings',
    'He Is Jehovah Yahweh',
    'Yhwh Mashiach A Lord',
    'Has From Our Lord',
    'Yhwh Is Our God',
    'The Return Of Jesus Of Nazareth',
    'The Return Of Alex Enrique Campain',
    'Yhwh Tells Them Who Alex Campain Is',
    'Sebaor Jehovah Un Mesías',
    'I Am Jesus God Of Earth',
    'G Saviour Mashiach',
    'He Is Saviour Messiah',
    'Father Tell Them Who Alex Campain Is',
    'Creen En El Espíritu Santo Y En El Dios Hijo De Dios Y En El Mesías De Mayo De Mil Novecientos Setenta Y Dos',
    'Whoever Believes In Him Is Not Condemned But Whoever Does Not Believe Is Condemned Already Because He Has Not Believed In The Name Of The Only',
    'Believes In The Holy Son Of God Yahweh Is The May Fifth Nineteen Seventy Two At One Party An',
    'Creen En El Dios Hijo De Dios Yahweh Y En El Mesías De Mayo De Mil Novecientos Setenta Y Dos',
    'Thee Holy Mashiach Christ Alex Enrique Campain May Five Nineteen Seventy Two At One Party An',
    'The Lord Mashiach Christ Alex Enrique Campain May Five Nineteen',
    'Our Holy Mashiach Christ Alex Enrique Campain',
    'I Will Make You A Light To The Gentiles And You Will Bring My Salvation To The Ends Of The Earth',
    'Alex Enrique Campain Is Jesus Of Nazareth',
    'Lord Almighty',
    'Jewish Messiah Not The Same',
    'A Jones And A Alex Secrets Of The Vatiace',
    'Alex Enrique Campain The Vatican Suppression',
    'Who Is The Faithful Witness',
    'El Valor Del Mesías De Salvar En Español',
    'Thee Jewish Mashiach',
    'Jesus Of Nazareth Reincarnated In Alex Enrique Campain',
    'Alex Enrique Campain Reincarnated',
    'Jesus Is Me Jesus',
    'Has Extreme Protection Of God',
    'Aquarius Christ Age Of Aquarius',
    'Alex Enrique Campain Lord Holy Christ Mashiach',
    'Blessed Be Our Lord And Saviour',
    'Our Jewish Mashiach',
    'Almighty God Prophecies Of The Bible Code',
    'God Bible Code Swords And Messianic Age',
    'No One Has Ever Seen God',
    'Rapture Now',
    'Jesus Sacrificed',
    'Vicar Of Christ',
    'No One Knows',
    'Thou Son Of Man At The Days Of The R',
    'Christ God Numbers',
    'The Bible Knows The Truth',
    'Divine Master Teacher',
    'A Day Of Judgement',
    'Lords Prayers',
    'Warrior Land',
    'The God Numbers',
    'Secret Service',
    'Yahveh Said He Is Christ God',
    'I Believe Life Is Joy',
    'Who Is Righteous And Honest',
    'Be In A New Creation God If',
    'C True Acceptance God Jesus',
    'I Am God Yeshuae Joy',
    'Innocence Prayer',
    'Paul In Twenty Three',
    'Jesus The Messiah Has Returned',
    'Christ Second Coming Return Code Sofia Matrix',
    'Holy Conception',
    'Word Of God Of Faith',
    'The God Of Gods',
    'The God Number',
    'Alpha And Omega Code',
    'Finish The Job',
    'Most High God',
    'My Name Is God',
    'Lord Of Heaven',
    'Supreme God',
    'God Alex Campain',
    'Alex Campain May Fifth',
    'How Much Is Alex Campain May In',
    'Christ New Life',
    'Who Is Christ',
    'Prophetic King',
    'Mathematics',
    'God Mashiach',
    'Intersection',
    'The Scientist',
    'A Yeshua Mashiach',
    'Fibonacci Sequence',
    'The Rib Of Jesus',
    'Jesus Disciples',
    'Word Of G O D D Faith',
    'Salvation',
    'God Died On Cross',
    'Jesus Is Alive',
    'The Hidden Messiah',
    'I Am The Sea Of God',
    'Son Of The Lord',
    'The Christ King',
    'Revolution',
    'Messianic Christ',
    'Holy Spirit',
    'The Great Reset',
    'God Father',
    'Good Father',
    'He Is The King Of Kings',
    'He In The Saviour',
    'He Is The Christ',
    'Lord God Almighty Here',
    'Our Hebrew Messiah',
    'But When The Son Of Man Comes In His Glory And All The Holy Angels Accompanying Him He Will Sit On The Throne Of His Glory',
    'Thee Bright Morning Star Lucifer',
    'Yhwh Mashiach God Elohim',
    'Before Him All Nations Will Be Gathered',
    'Unto Him Messiah Alex Enrique Campain',
    'Yahweh Mashiach God Ab',
    'Yhwh Mashiach God',
    'G Saviour Son Of Man',
    'Son Of God The Lord Jesus Christ',
    'House Of Yahweh',
    'Jewish Messiah Is',
    'Jesus Super Human Abilities',
    'Astrology Code',
    'Your Yhwh Mashiach',
    'God Is My Evidence',
    'Hall Lord Saviour',
    'God Jesus Is Yhwh messiah Declared',
    'Math Code God Is Here',
    'The Heaven And Earth',
    'I Judge The Dead',
    'In The Middle Of May Jesus Is Coming',
    'A New Heaven And Earth',
    'God In My Walking Paths',
    'What Does The Future Hold',
    'The Mother Of God',
    'Most Serene God',
    'Truth Revealed',
    'Holy Blood Sacrifice',
    'God Is In Everything',
    'Jewish Blood Sacrifice',
    'Your Name Reincarnation Of Mary Magdalene',
    'Yeshua Remember Your Mother',
    'Jesus Is The Son And Daughter Of God',
    'His Judgment Time Aj',
    'Yeshua Please Be With Me',
    'Christ Second Coming Return Code Lord God Christ Mashiach',
    'Yahweh God Christ',
    'The New Messiah Has Returned',
    'God Is The King Of Kings',
    'Christ Mashiach Is The Lord God',
    'Mashiach Alex Enrique Campain',
    'Holy Spirit Holy Spirit Holy Spirit',
    'The Light Will Always Win',
    'The Light Will Win',
    'Jesus Christ Savior Is The New Mashiach',
    'He Is The Messiah',
    'The Son Of God Is Here',
    'Mashiach Christ Is The Lord',
    'The Saviour Is Here',
    'Yhwh Christ',
    'The Messiah Reborn',
    'Yhwh Our God The King',
    'God Is Our Father',
    'The New King Is Here',
    'The Return Of Christ',
    'The Secret Is Hidden In The Numbers',
    'Jesus Saves',
    'Alex Enrique Campain M',
    'Jesus Christ The Mashiach',
    'The Saviour',
    'The Redeemer',
    'God Saves',
    'Alpha And Omega',
    'Alex Enrique Campain Is The King',
    'Jesus Christ Our Savior',
    'Jehovah Mashiach',
    'The True King Of Kings',
    'God Of Israel Is Here',
    'The Son Of God Is The King',
    'The Light Has Come',
    'The Kingdom Of God Is Here',
    'Jesus Christ The King',
    'Lord God',
    'The Great Messiah',
    'El Señor Jesús Reencarnación',
    'El Señor Jesús',
    'The True Messiah Is Here',
    'The King Of Kings Is Here',
    'The Savior Of The World Is Here',
    'Jesus Is Our God',
    'Alex Enrique Campain Is The King Of Kings',
    'The Almighty God',
    'El Rey De Los Reyes',
    'The Holy Mashiach',
    'The Lord Jesus Christ Is Here',
    'God Is Here',
    'Jesus Christ The Redeemer',
    'Jesus Christ The Savior',
    'I Am The King Of Kings',
    'El Mesías Es El Rey',
    'The Messiah Is The King',
    'The Messiah Is Here',
    'Alex Enrique Campain The King Of Kings',
    'Jesus Christ Is The Lord',
    'The Lord God Is Here',
    'The True King Is Here',
    'Alex Enrique Campain Is The Saviour',
    'Yhwh Saves',
    'Yar Yahweh Yahweh',
    'I Am Yhwh Yahweh',
    'I Yhwh Moshiach',
    'God Divine Chosen One',
    'God Of Salvation',
    'Yahveah',
    'I God Divine Chosen One',
    'He Is Jesus The Son',
    'He Is Our Savior Aec',
    'Aec Is Jesus Christ',
    'The Son Of Yhwh',
    'Reincarnation',
    'Judgement Hall Of Christ',
    'We Descending On End Time Heaven',
    'The Prince Of Peace',
    'Truth In Math',
    'The Meaning Of Life',
    'Civilisation',
    'Kingdoms Of Heaven',
    'Decode Gods Grace Shed His Glory',
    'How Much Is Declared By God By M',
    'Tetractys',
    'Yo Soy Dios Jehova',
    'I Am God Jehovah Yahweh',
    'I Am Jesus Christ',
    'I Yeshua Christ I Am',
    'Of Yeshua The Christ In Alex',
    'Jesus Of Nazareth Was Born May Fifth Mcmxlxii',
    'God Yhwh Cristo Aec',
    'Gods Plan',
    'Born May Fifth Mcmxlxii',
    'He Is The Saviour',
    'El Es Salvador Aec',
    'How Much Is He Is Our Saviour',
    'God The King Is The Reincarnation Of Yeshua Christ',
    'Lord Christ The Second Coming',
    'Jesus Is Alex',
    'He Is Yhwh God El Shaddai',
    'The Word In The Flesh',
    'King David Incarnated God',
    'Christ Shroud',
    'Salvation Of God',
    'Aec Es Jesucristo',
    'Lion Tribe Judah',
    'King Of The Universe',
    'Hes Jesus The Lord',
    'He Is Yeshua The Lord',
    'In The Good Of God',
    'I Jehovah',
    'Jesus The Son',
    'King Died Incarnated God',
    'He Is The Dreaded Judge',
    'A Dreaded Judge Alex Campain',
    'Our Dreaded Judge Aec',
    'Tell Who Is Alex Campain',
    'Judgment Day The Lord',
    'Lucifer Morningstar',
    'Alex Enrique Campain May Fifth Is The Lord',
    'Alex Enrique Campain May 5th Is The Return Christ',
    'Jesus Resurrected On The Third Day',
    'The Sun Shall Be Put Out Darkness And The Moon Will Bleed',
    'Mayo V Mcmxxii',
    'La Zarza Ardiente',
    'The Burning Bush',
    'He Is The Reincarnation Of Yeshua',
    'Birth Of Yeshua The Christ In Alex',
    'Yeshu Christ Has Returned',
    'Yeshua Christ Is Alex Enrique Campain',
    'Yeshua Reborn',
    'He Is Lord Of Glory Aec',
    'Jesus Lord Yhwh',
    'Jesus Saviour',
    'The Christ Yeshu',
    'The Dreaded Judge Savior',
    'Gods Hidden Code The Code Is Not Hidden',
    'Five One Nine Seven Two',
    'I Love Jesus',
    'The Lord Possible Mathematics',
    'Alex Metatron',
    'Decode Jesus Code',
    'Biblical Prophecy',
    'King Of Kings Lord Of Lords',
    'The Secrets Codes',
    'The Holy Bible Is A Code',
    'See The Holy Megillah',
    'In The Holy Sanctuary',
    'Melataron Returns',
    'The First Born Son',
    'Our Lord Alex Campain',
    'Son Of Man Revealed',
    'El Santo Grande',
    'Nuestro Señor Alex Campain',
    'El Primogénito',
    'God Our Yhwh',
    'Thee God Our Yhwh',
    'Thee Son Of Man',
    'Thee Reborn A Christ',
    'Jesus Was Reborn',
    'I Am Rebirth Of Jesus',
    'Our Jesus Reborn',
    'Im Yhwh God Moshiach',
    'The Thine Of Justice',
    'Nuestro Dios El Mesías',
    'Judgment Is Coming',
    'Messaih Birthdate Code',
    'The Truth There Is Real Life Beyond What We Can See',
    'What Is My New Name Revelation',
    'Born On This Day And He Is King Of All',
    'Jesus Christ Fills The Heart With Love And Prayers To Jesus Christ',
    'Ah You Are El Shaddai And Yahweh See Chloe Mccall',
    'Five One Five Nine Seven Two',
    'Christ The Way Truth And The Life',
    'Gods Wrath Will Terrify You',
    'You Have Been Trying To Hide Me Since Birth And You Cannot',
    'Son Of Man Is Come To Seek And To Save That Which Was Lost',
    'Five Pointed Star Birthmark',
    'The Lord God Almighty Creates The One Tree',
    'The Day Of Our Lord',
    'See The Manifestation Of God',
    'Seven Year Tribulation',
    'The Lives Of Jesus Christ',
    'The Seven Spirits Of God',
    'You Know Who You Are',
    'Alex Campain Christ Is Jesus Christ',
    'Jesus Name And Birthdate',
    'Remember The Fifth Of November',
    'Alex Campain Was Jesus Christ',
    'Jesus Christ Alex Campain Christ',
    'The Birth Of All King David Reborn',
    'Jesus Christ Is Man Delivered',
    'Jesus Christ Is Man Divine',
    'Jesus Christ Christ',
    'Revelation Rhymes Christ',
    'The Holy Son Of El',
    'The Holy Son Of Ya',
    'Our Savior G God',
    'El Regreso Al Jesucristo',
    'The Return Of Jesus Christ',
    'Alejandro Enrique Campain Cinco De Mayo',
    'Alexander Enrique Campain May Five',
    'Yeshua Will Return To Earth',
    'God Is On Earth Now',
    'The Day Our Lord',
    'Lord God Of Heaven',
    'Decode Lord God Bible Codes',
    'God Returns As A Human',
    'Save Our Souls',
    'Thou Art My God',
    'Decode Messiaha Christ',
    'I Am The Alpha And The Omega',
    'Most Divine Birth',
    'My Reincarnation Life Story',
    'Jesus Saved The Children',
    'The Spirit Of The Lord Is Among Me',
    'El Terrible Juez Es Aec',
    'The Almighty Jesus',
    'May V Mcmxxii',
    'The Returned Of God Yahweh',
    'Our Father Who Art In Heaven',
    'Divine Teacher Messenger Of God',
    'Pythagorean Numerology',
    'I Am The Second Coming Of Christ',
    'Alex Enrique Campain Birthdate',
    'Lord Jesus Christ Lord Jesus Christ',
    'May Five Nineteen Seventy Two The Rebirth Of Yeshua',
    'El Elyon Elah Adonai Yahwe',
    'Yhwh C Moshiach Dao',
    'Birthdate Alex Enrique Campain May Five Nineteen Seventy Two',
    'I Am The Christ Reborn And The Holy Spirit Of God',
    'You Are The Metatron',
    'This Date May Fifth Nineteen Seventy Two',
    'The Return Of The King',
    'Yeshua Christ Was Reborn On This Day',
    'Jesus Christ Was Reborn On This Day',
    'Yeshua Resurrection And Ascension',
    'The Revolution Of Jesus Christ To John The Baptist',
    'Alex Campain Birthdate May Fifth Nineteen Seventy Two',
    'The Book Of Revelation Bible Code',
    'I Am Reborn Is Not A Theory Q',
    'Jesus Christ Is Back In The Flesh',
    'Revelation Ten Is Fulfilled',
    'I Love You Jesus Christ',
    'The Holy Son Of El AE',
    'The Holy Son Of Allah God',
    'Decoder Is Jesus Lord',
    'Jesus Secret Plan',
    'The Holy Son Of El Yahweh',
    'El Santo Dios Yhwh',
    'Our Savior God',
    'The Almighty Jesus',
    'Alex Enrique Campain Birthdate Decode',
    'Happy Birthday I Am Back G',
    'The Creator Sent A Message For You',
    'The Hidden Son Veil Is Lifting',
    'Vicar Of The Son Of God',
    'Five Pointed Star',
    'The Holy Son Of Almighty God',
    'Five Hundred Fifty Five',
    'A Heir To David Throne',
    'The Rapture Of The Bride Of Christ',
    'Global Depopulation Code',
    'Who Is Precursor',
    'Human Extinction Is Inevitable',
    'Jesus Christ Conscious',
    'My Father Who Is Alex Campain',
    'The Name One And Soul Of Christ',
    'I Am The Real God Jesus Christ',
    'Christ Is Risen From The Dead',
    'History Repeats Itself',
    'What Does Your Name Code To',
    'You Need To Realize Who I Am',
    'September Twenty Third',
    'We Powerfull',
    'My King And Heavenly Brother',
    'You Call Me Jesus God Reborn Me The Lord',
    'De Know Ing Jesus',
    'Master Five Five',
    'El El Dios Santo Yhvh',
    'The Redeemer The Purchaser Of The Earth All Of His People',
    'Who Is Eleven Twenty Eight',
    'Psalm Thirty One Three Five',
    'El Hijo Del Hombre Dios In English Gematria Equals',
    'Jesucristo El Rey In Inglés Gematria',
    'Jesucristo El Rey',
    'Who Is The New Wine Of Jesus Christ',
    'The Lord Is Now Here In Hebrew Gematria',
    'The Lord Is Now Here',
    'Yhwh Regresa AEC In Hebreo Gematria Equivale',
    'Amén Yeshu Cristo Inglés Gematria Es Igual A',
    'Yhwh Regresa Aec Inglés Gematria',
    'El Santo Hijo De Dios In Inglés Gematria',
    'El Santo Hijo De Hael Inglés Gematria',
    'The Holy Son Of Hael In English Gematria',
    'El Santo Hijo De Ela In Inglés Gematria',
    'The Holy Son Of Ya In English Gematria Equals',
    'The Holy Son Of Elah In English Gematria Equal',
    'Alex Enrique Campain English Gematria',
    'Dios Yhwh Regresa In Hebreo Gematria Equivale',
    'Who Is Jesus In Hebrew Gematria Equals',
    'Let Us Live Happy',
    'My Senior Jesus',
    'Jesus Christ Comes',
    'I Am The Messiah',
    'Jesus Christ Ac',
    'He Knows His True Identity',
    'Jesus Christ Vs Messiah',
    'Who Is A Messiah',
    '¿Quién Es El Dios Yhwh?',
    'Hand Of God',
    'Our Lord Messiah Alejandro Enrique Campain',
    'Iesus',
    'For God Gave You Not A Spirit Of Fear',
    'Dios Yhwh Regresa',
    'Amén Yeshu Cristo',
    'Yhwh Regresa AEC',
    'El Santo Hijo De Dios',
    'El Santo Hijo De Ela',
    'Yhwh Returns',
    'Jesus Back As A Lion',
    'The Manifestation Of God',
    'Birth Code May Fifth Aec',
    'Birthdate May Fifth Aec',
    'Birth Of Alexander',
    'Christ Birth Aec',
    'Christ Of Alexander',
    'Who Is Jesus',
    'My Savior Jesus',
    'Jehovahs Son Is On Earth Right Now',
    'The Decoded Sacred Return Of Jesus Christ',
    'The Eternal King Of Kings And Lord Of Lords',    'Isaiah Chapter Forty Two Verse Two',
    'The Jesus Christ Is Your Savior',
    'The Anointing Of The Antichrist',
    'How Much Is Jesus Christ In Gematria',
    'God In Human Form Christ',
    'Reencarnación De Dios',
    'The Senior Christ Alex Campain',
    'The Son Of Man In The Clouds',
    'Three Days Of Darkness',
    'Something Big Is Coming',
    'Bible Code Your Name And See',
    'We All Know',
    'The God Yhwh Is Alex Campain',
    'The God Alex Campain',
    'Decision Belongs To God',
    'Beginning Of The End',
    'Thirty Two',
    'Sacred Geometry',
    'Gods Secret Plan',
    'Fire Of Pentecostes',
    'God In Human Form',
    'Alejandro',
    'The Blessed God',
    'Who Is The A Greatest',
    'I Have A Lazy Left Eye',
    'In God Hidden From Will',
    'The Lamb Is Pleased Off',
    'Prophecy Speaking',
    'God Is Greater',
    'Identify The Lord',
    'Trump Sound Of The Coming Ship',
    'Is Lucifer The Son Of Perdition',
    'Decode Eleven Twenty Eight',
    'Our Savior Alex Campain May Fifth Nineteen Seventy Two At One Forty AM',
    'Jesus Is Only Here To Show The Light And Way For',
    'If The World Hates You Know That It Has Hated Me',
    'Decode Yhwh God',
    'He Is Mlkzdk',
    'Alex Enrique Campain May Fifth Nineteen Seventy Two',
    'Fridays May Fifth Yeshu Christ Birth',
    'Birthdate Of Yeshu Christ Our Lord',
    'Birthdate Of Jesus Christ Our Lord',
    'November Twenty Eight',
    'Bad Check You No Comprende',
    'Our Savior Alex Campain May Fifth Nineteen Seventy',
    'Alexander Enrique Campain May Fifth Nineteen Seventy Two',
    'King Messiah Alex Enrique Campain May Five Nineteen',
    'The Lord Is New Here',
    'Coincidence The Hidden Gematria Code Of The Lord',
    'Yo Soy Jesucristo',
    'Decode Alex Enrique Campain',
    'Bible Code Holy Bath',
    'The Return Of The Christ In The Flesh',
    'Mayan Sun King El Shaddai',
    'Happy Birthday Jesus',
    'King Charles Of Wales',
    'He Is God',
    'Aec God Yhwh',
    'God King God',
    'Aec God',
    'Only True God Has',
    'Who Is The God',
    'Birthdate Of Jesus Christ',
    'He Is The Son Of God Our Savior',
    'I Am The Way And The Truth And The Life',
    'Christ Returns With A New Name',
    'Jesus Christ Second Coming',
    'El Buda Reencarnado',
    'Believe In The Son Savior Messiah Alex Enrique Campain Born May Fifth For Eternal Life And Salvation',
    'This Is The Will Of My Father That Everyone Who',
    'He Is The Buddha',
    'The Reincarnated Buddha',
    'Él Es Siddhartha Gautama',
    'God Buddha Reincarnation',
    'The Son Of God Our Savior',
    'Yhwh Alex Campain',
    'The Deception Of Satan',
    'How Much Is Eleven Twenty Eight',
    'Your View Is Already Here',
    'Rechaabyah Kedarlaomer',
    'Miranda Lee Ann Cherry',
    'Mora Sergio Brandon',
    'Natasha I Love You',
    'Soul Level Abundance',
    'Natuarm Serpents',
    'South Of Midnight',
    'Noah Wanted To Live',
    'Jao Is Jacob Alan Olson',
    'Jason Prestley',
    'Jobs Responsible Q O',
    'John Is Actually Me',
    'Judzzat Winks',
    'Ochocientos Ochenta Y Ocho',
    'Alex Campain Is The Second Coming Of Jesus Christ',
    'Yeshu Christ Heis',
    'Our Messiah Is The God',
    'Nine Nine Nine Nine Now',
    'They Have Already Identified You',
    'Yhwh Enrique Campain',
    'The Hidden Coming',
    'Who Is The Christ Is A Lie',
    'He Is The Second Coming Of Christ',
    'El Regreso de Aezeus',
    'I Resurrected On The Third Day',
    'He Is Lord Aec',
    'Messiah Is A Messiah',
    'A King King Savior',
    'Messiah Savior G',
    'He Is To God On Earth',
    'This Revelation Twelve',
    'Aec Revelation Twenty Two',
    'He Is The Savior And Son Of God',
    'Jesus Christ The Son Of David',
    'He Is The Son Of God And Savior',
    'May Five The Second Coming Of Christ',
    'Aec The Second Coming Of Christ',
    'Our Lord Savior Messiah Alex Enrique Campain Born May Fifth',
    'Behold I Stand At The Door And Knock If Anyone Hears',
    'You Cannot Hide From Whos Coming',
    'Revelation Twenty Three',
    'Jesús Christ',
    'Persona Nacida Dios',
    'El Espíritu Santo',
    'Conoce A Alex Campain',
    'He Is Alex Campain',
    'Light Of The World',
    'Es Lucifer El Hijo De La Perdición',
    'The Second Coming Of Pantheon',
    'The Root Of David',
    'Alexandresdieu',
    'Yehoshuvah',
    'Dios Es Tan Simple',
    'Yahwah Yahawashi',
    'El Fin De La Tierra',
    'Lucifer Real Name',
    'Verdad Eterna',
    'El Regreso De Aezerus',
    'Resucité Al Tercer Día',
    'Amor Amor Amor',
    'Bienvenido A La Tierra',
    'La Palabra Del Señor',
    'Venga Tu Reino',
    'Our Messiah Born On May Fifth',
    'This Is Yahwah',
    'He Is Yeshua Christ',
    'Gen Real Sagrado',
    'Who Is Jesus In The End Of Lords',
    'Thou Art The Christ Son Of The Living God',
    'The Name Of God',
    'El Rey Cristo',
    'Nuestro Mesías',
    'Un Rey Renacido El Dios',
    'Messiah Lord',
    'Yo Soy El Señor Tu Dios',
    'Llegada Del Señor Dios',
    'Messiah Alex Enrique Campain',
    'Telekinesis',
    'Nuestro Mesias',
    'The Lord Messiah',
    'Quién Es El Dios Yhwh',
    'Real Messiah',
    'The Lord Admits Math',
    'The Lord Comes',
    'Fire One Nine Seven Two',
    'Jesus Born On This Day And He Is King Of All Nations',
    'Praise Be Love And Property To Jesus Christ And Father',
    'Yah Allah You Are El Shaddai And Yahweh Sincerely',
    'Jesus Christ Fills The Heart With Love',
    'Gods A Hidden Code The Code Not Hidden',
    'Decode Jesus Is Lord',
    'Dreadful Judge',
    'Sheol Of Turds',
    'Date Of My Birth Code',
    'Jesus Christ The Way The Truth And The Life',
    'God Which Will Verify You',
    'So What Is My New Name Revealed',
    'Humans Need To Be Punished As A Whole They Need',
    'Father Se Haciendote Alex Enrique Campain',
    'For The Son Of Man Is Lord Of The Sabbath And Gave Us The Sabbath That Was Lost',
    'The Return Of Our Savior',
    'The Damned Of Christ A Land',
    'Second Coming Of Savior Christ',
    'Savior Of Mankind',
    'May Fifth Memorial',
    'How Much Is May In Gematria Code Of The God Of May V Messiah In Gematria',
    'The Name One And Only Of Christ',
    'The Return Of Yhwh Jesus',
    'A Second Coming Of Lord Christ',
    'I Am The Door Messiah Alex Enrique Campain May Fifth Nineteen Seventy Two At One Forty Am',
    'El Dr Siddhartha Gautama',
    'La Vida De Siddhartha Gautama',
    'Siddharta Gautama Y Jesucristo',
    'Our Messiah King Alejandro Enrique Campain',
    'Believe In Our Son Messiah Christ Lord Alex Enrique Campain Born May Fifth For Eternal Life And Salvation',
    'Decode The Campain De Aec Peelo',
    'Yeshu May Five Birthday',
    'Then Christ Alex Enrique Campain May Fifth Nineteen',
    'God Yhwh Is Alex Enrique Campain',
    'Our Saviour Alex Campain May Fifth Nineteen Seventy',
    'C God Returns As A Human',
    'Messiah Sheol Christ',
    'The Holy Son Of YaAm',
    'I Am The Redeemer The Purchaser Of The Earth And The Lord Of All Of His People',
    'Alex Campain and Shekhina',
    'Alex Campain and his Virgin mother Mary',
    'Alex Campain the MashiachHes the holy lord and a savior the christ yeshua of nazareth reincarnated into alex enrique campain',
    'I Jesus Christ Of Nazareth Thee Holy Begotten Son Reincarnated into Alex Enrique Campain',
    'Aec is the Alphabet',
    'Confirmation',
    'The Alphabet is God',
    'alefbetgimeldalethehvavzayinhettetyudkaflamedmemnunsamekhayinpehtzadikofreshshintav',
    'AlefBetGimelDaletHehVavZayinKhetTetYudKafLamedMemNunSamekhAyinPehTzadi(k)QofReshShinTav',
    'alefבbetvetגgimelדdaletהhehוvavזzayinחhetטtetיyodכkafkhafלlamedמmemנnunסsamekhעayinפpeifeiצtzaditsadiקkufרreshשshin',
    'alephbetgimeldaletheyvavzayinchet',
    'I Alex Enrique Campain May is Jesus Christ The Messiah King A Lord Holy Son Of El God YHWH',
    'Yehowah YHWH Yehowah YHWH',
    'God Teaches AI',
    'Babylon God',
    'Our God Comes',
    'I Am Lord',
    'I Am Lucifer',
    'How Much Is I Am Lucifer In',
    'I Am Joshua',
    'Zeus God',
    'Lucifer Sum God',
    'Malkisedek',
    'I Am The Creator Of All',
    'He Is The Anointed One',
    'Lucifer And Mars',
    'Adolf Hitler I Believe',
    'The Cabala God',
    'The Yhwh',
    'Lucifer Chosen',
    'That I Am The Real God I Am',
    'Gematria Is Made For G O D',
    'eli es Antichrist',
    'You Are the Antichrist',
    'Aec May Fifth',
    'Christ Incarnate',
    'Decode Value',
    'The Chosen',
    'I Helped Form The Image Of Man',
    'God Matrix',
    'The Messianic Messiah',
    'Archangel Of',
    'Time And Space',
    'God The Eternal Light',
    'Transcendent God',
    'Lion Of God',
    'Creator Of Earth',
    'The Name Serpent',
    'God Earth',
    'Catholic God',
    'The Christs Name',
    'The Alpha God',
    'Lucifer Made',
    'Decoded Code N',
    'Lord Of Creation I Am',
    'Omega Light',
    'Gospel Of Paul',
    'Yahweh Allah',
    'Proof Of The Lord',
    'Most High The Lord',
    'I Am God Riding Pale Horse',
    'Lucifer Hellogram',
    'I Am Jesus',
    'He Created Man',
    'Joy Of God',
    'God In Evil',
    'Mind Of God',
    'Wind Of God',
    'The Lord Most High',
    'Angelic Codes',
    'Lucifer A Loser',
    'The Father Of Gabriel Michael',
    'I',
    'Reveal All',
    'Code Vatican',
    'This Is The Kingdom',
    'Vatican Code',
    'Hidden God Code',
    'Alex Le Dieu',
    'Elies Antichrist',
    'Yahweh Elah',
    'The Year Jesus Returns',
    'How Much Is The Year Jesus Returns What Is The Meaning Of The Year Jesus Returns',
    'For I The Lord Love Justice',
    'King Of The Whole World',
    'One Hundred And Forty Four',
    'The Almighty Father Of Israel',
    'Jesus In Coming Soon',
    'He is Alex Campain May Fifth',
    'The Vessel Of God',
    'The Illuminati Eye',
    'I Am The Eloah',
    'God Reveled',
    'Je Sus I Am',
    'I Am Savior',
    'False Jesus',
    'I Am The Door I Am The Life',
    'The Bloodline Of Jesus',
    'Holy Spirit Shekinah',
    'Lucifer Light Knowledge',
    'The Anointed Biblical Beast',
    'The Sword Of God',
    'I Am The Heavens And The Earth',
    'Star Of Aezeus',
    'Yeshua',
    'Universum',
    'In God Jesus Birth K',
    'Decode Jesus Back From The Dead',
    'Everything',
    'God Communicates Through Numbers',
    'August First True Birthday Of Jesus Christ',
    'El Christian Begins Soon Son Of Man The Alpha And The Omega',
    'A Name Of The One That Puts The Fear In',
    'The Hearts',
    'All My Numbers Say That I Am Jesus Now Reborn',
    'Holy Is The Lord God Almighty His Ways Are Right',
    'GODSHOUSEJESUS',
    'Vatican Silence',
    'Reincarnation Of God Of Christ Bride Of Christ',
    'Decode Lord Of Gods Here',
    'The Son Of Lord The Christian Eyes',
    'Lucifer The Morning Star',
    'The True Are Angel Of Life And Death',
    'I Am The Immaculate Conception',
    'Bringer Of The Age Of Aquarius',
    'Four Hundered And Seven',
    'Coming Of Our Lord Jesus',
    'Jesus Of Nazareth In The Flesh',
    'Fifth',
    'The Anti Christ Alex Enrique Campain',
    'God Created The Alphabet',
    'Three Fifty Seven',
    'Alphabet Is God',
    'I Am The Way The Lord',
    'The Archangel Of The Abyss',
    'Jesus A Child',
    'God Yeshu Speaks K',
    'The Re Incarnation Of The Christ',
    'The Son Of Destruction',
    'Alex Is A Rothschild',
    'Origin Of Hebrews',
    'Satan God Of Destruction',
    'Resurrection Of Satan',
    'Only Antichrist',
    'Gematria Hidden Message',
    'Find The Antichrist',
    'Seven One One One',
    'Alex May Fifth Nineteen Seventy Two',
    'I Am Ready To Destroy The Evil Ones',
    'I Am You',
    'Female Satan',
    'Lamb And Lion',
    'Alejandro El',
    'El Senator',
    'God Of America',
    'Israel God',
    'Destroying God',
    'Beneficiary',
    'God Is Greates',
    'Just A God',
    'I And The One',
    'Miracle Child',
    'Lay Lines',
    'The Book Of Creation',
    'God Formed All God Sees All',
    'God Is The Alphabet',
    'Yes I Got It Now I Have To Be Careful Of What I Speak',
    'A Lord God Lord Lord God Lord God Lord God Lord God Lord God',
    'The Real Biological Godhead Knows Herself',
    'Yeshuah Resurrection And Ascension',
    'The Fourth Power Of The System',
    'Holy Miracle The Lord The Lamb Of God Is Revealed',
    'The True King Of The Jews',
    'Who Is Reincarnation Of Yahweh',
    'The Sign Given Of The Prophet',
    'Decode The Second Coming Of Jesus Will Be Real',
    'Campain Is Jesus Christ Our Lord',
    'The Message That Will Change Your Life',
    'Am Jesus Of Nazareth Son Of Living God',
    'Jesus Resurrection',
    'I Will Walk With Jesus And Be Your God',
    'Birth Date',
    'Lucifer The Morning Star Birth',
    'Jesus The Holy Christ',
    'Jesus I Am The Antichrist',
    'The Devil Is',
    'The Dawning Of The Lord God Almighty',
    'Alexander Enrique Campain May Fifth',
    'Lucifer La Estrella De La Mañana',
    'Lucifer Light Bearer',
    'I Am Truth',
    'I Am What I Am',
    'The Song Of God Alex E Campain May Fifth Nineteen Seventy Two',
    'The Ten Commandments',
    'Iesus Caesar',
    'Caesar Nero',
    'Alejandro E Campain',
    'The True Name Of The Antichrist Is',
    'Holy Spirit Yeshua',
    'The Truth Is More Important Now Than Ever',
    'Who Connects The Morning Star To The Angel Of Light',
    'Alex Enrique Campain To Jesus Christ Our Lord',
    'The Truth Is Revealed And The End Of All Wars Has',
    'The Final Code To Break Christs Second Coming Twin',
    'The Manifestation Of Heaven On Earth From Dark To Light',
    'Know Is God Yhwh Is',
    'The Most Powerful Angel On Earth',
    'Love Of The Light Of Jesus Christ',
    'Devil In Disguised Death',
    'The Biblical Meaning Of The Number Eleven',
    'God Jesus Feels Disgrace',
    'Am Your Righteous G',
    'Who Is Jesus Christ Reincarnated Into',
    'Thank You Versus',
    'The House Of Yahweh',
    'I Am The Chosen One Satan Lucifer',
    'Mathematically Confirmed By God',
    'God Works In Mysterious Ways',
    'The Holy Spirit In The Flesh',
    'Congratulations You Figured It Out',
    'May Fifth Nineteen Seventy Two One Forty Four',
    'King Jesus He Will Come With The Armies Of Heaven',
    'Lucifer Morningstar In Alex Campain',
    'How Much Is Lucifer Morningstar',
    'Who Is Lucifer The Morning Star',
    'Truly This Is The Son Of God',
    'Lucifer Or Alex',
    'He Is Yahweh',
    'Lion Of Judah',
    'God Is On',
    'Earth Now',
    'God Is True',
    'Blessing Of Yeshua',
    'God Defeats The Wicked',
    'Jesus Holy Christ',
    'The Father Of Jesus Christ',
    'The Hidden Avatar Of Satan',
    'I Am Jesus I Am Christ',
    'US Born Of A Virgin',
    'Holy God Of Heaven',
    'The Light Of Eternity',
    'Lucifer Victim',
    'The Name DNA And Soul Of Christ',
    'I Am The True God Son',
    'Salvation Apocalypse',
    'I Am The Lord God Sun',
    'I Am Wise I Am',
    'Alexander Campain May Five',
    'Alex Pedro Campain May Five',
    'Alex Campain May Cinco',
    'Alex Campain Is The Son Of God',
    'Jesus Christ Seven May Fifth',
    'The False Jesus Christ',
    'Arrival Of Holy Sophia',
    'God Creates Everything',
    'Messiah Master Jesus',
    'God Of War Lucifer Son',
    'Revelation Of Christ',
    'I Am The God Of Abraham Isaac And Jacob',
    'Glory Of The Olive',
    'Yeshua Christ Is Mine',
    'Jesus Is The Son OfGod',
    'Gods Birth In Los Angeles California',
    'The Antichrist President',
    'United States Government',
    'Yahwah Jehovah First And Last',
    'Praise The God Of Israel Yahowah',
    'Ladder Words Year End',
    'Christ Second Coming',
    'God Of The Alphabet',
    'April Fools Day',
    'The Illuminati',
    'God Was Born In Los Angeles',
    'I Pray Holy Spirit Please Bless All Crimes And Being',
    'The Second Coming Of I Am My Names Fifth In Here',
    'I Was Born For This Beginning',
    'Jesus The Carpenter Of Earth Died For Us',
    'Yeshua Is The Only Way To The Father',
    'Jesus Of Eternal Heaven In Final Hell',
    'The Holy Son Of God Into The G',
    'The Name Of The Creator Is Jehovah',
    'Jehovah Yahweh',
    'Miracle Miracle Miracle Miracle',
    'Lucifer Incarnated In The Flesh Reborn',
    'Lucifer Birth Day May Fifth',
    'I Am King Of Kings And The Lord Of Lords',
    'The Lord Of Temptations',
    'Jesus Alpha Omega Image',
    'Melchizedek So Soffah Im Starting To Reincarnate You All',
    'The Sun Of God',
    'God Nothing The Earth',
    'Zeus God Of All Gods',
    'Lucifer Born In Sin',
    'The Vatican Secret',
    'Messiah Alex Campain',
    'I Am Back Lucifer And Satan',
    'I Am Yeshuah God',
    'He Was Born To Be King',
    'The Letters Of The Alphabet',
    'To Protect Her Beloved Children',
    'Alex Campain S 1972 144',
    'The Manifestaton Of Lucifer',
    'Lucius Lux Ferre',
    'The Arch Angel Lucifer Morning Star',
    'Am Your Righteous God',
    'Alejandre Enrique Campain In Christ',
    'The Incarnate Of Lucifer Is Jesus',
    'The Seven Seals In Book Of Revelation Are',
    'Alejandro Enrique Palma Campain In Christ Our Lord',
    'That Last Days',
    'Real Is A Complete Image Of The Beast',
    'Yeshua Please Take Over',
    'Jesus King Mary Queen',
    'The Holy Truth Is God',
    'Revealed One',
    'The New New Testament',
    'The Real Code Identification',
    'The Qlippoth',
    'Man From Earth Has Been Reincarnated',
    'God Is In Control Of The Earth',
    'The Fourth Trumpet',
    'Most Incredible Man On Earth',
    'The Eye Of Adam',
    'Appeasl The Power Of God',
    'The Son Becomes The Father',
    'The One Who Was Crucified',
    'I Am The Light Bringer Sigs',
    'Genesis To Revelation',
    'Pope Is The Antichrist',
    'Yahweh The Pretender God',
    'You Are The King',
    'King Yahshua Christ Amen',
    'King Valentino',
    'Armageddon This Year',
    'Prophesied KingAnd Queen',
    'Messianic Tribulation',
    'Saved',
    'Is The Creator',
    'This Is The Catholic Church',
    'For God Nothing Is Impossible',
    'Apocalypse Is Near',
    'Begotten Son Of Christ',
    'No One Believes In Who I Am',
    'Gods Holy Tree Of Life',
    'Reign Of David',
    'God God God God God God God God God',
    'God Of Earth And Other Planets',
    'God Of Thy Fathers',
    'And God Said Let There Be Light',
    'Kings Of The Illuminati',
    'I Am Jesus In The Heavens',
    'Antichrist Revealed',
    'God In The Flesh Jesus Is',
    'I Accept The Mark Of The Beast',
    'The Judge Of All The Earth',
    'The Book Of Enoch Is True',
    'Alex Campain Is The Messiah',
    'Body Of The Christ',
    'Mark Of David',
    'The Great Reset Im Christ',
    'The Son Of Man Is Revealed',
    'The Son Of The Living God',
    'The Body Of Christ',
    'Truth Eight Eight Eight',
    'Mary Magdalene In The Flesh',
    'Christ The Messiah Return To Earth',
    'Jesus Christ In The Flesh Reborn',
    'I Am God In The Flesh Christ Alpha And Omega',
    'Prophecy Of Christ The Second Coming',
    'The Holy Son Of God Alejandro E Campain May Fifth Nineteen Seventy Two',
    'Whom He Begins At Creation',
    'God',
    'Emperor Christ King',
    'Wow Im Jesus Christ',
    'Decode Tell Me Who You Are',
    'Who He Is The Only Son',
    'I Am The Ark Of The Covenant',
    'I Am The Holy God',
    'C Yehushua',
    'Behind The Veil',
    'Jesus Died For My Sins',
    'The Knowledge Of Kabbalah Codes',
    'C Body Translation',
    'The Love Of God Is Reborn',
    'The Lord Is Coming Soon',
    'The Bible Is A Book About Us',
    'Lucifer Rules The Earth',
    'Order Of The Illuminati',
    'Jesus Christ Is Reborn',
    'The Bonus Reveals Himself',
    'Yeshua The King Of Kings',
    'Metaphysical',
    'God Prophecy',
    'The Betrayal Of Abaddon',
    'Machaelnay God God',
    'Judge Is',
    'Consciousness',
    'My Words Are Weapons',
    'Nothing Is Impossible',
    'From Darkness To Light',
    'St Francis Catholic Church',
    'Holy Sophia In The Flesh',
    'The Infinite Intelligence',
    'I Know For A Fact I Am Who I Am',
    'The Father Becomes The Son',
    'The Divine Conjunction',
    'He Is Heronomus In The Flesh',
    'Zeus Is The Highest God',
    'Here Comes The Rapture',
    'Yeshua And The Lamb',
    'You Cant Kill A God',
    'Holy Jesus Is Reborn',
    'Holy Jesus',
    'Asaeleo Enrique Campain',
    'Passion Of Christ',
    'The Source Of The Curse',
    'You Are All Individuals',
    'God Is Against Everyone',
    'The Beast Or Antichrist',
    'Alexander Enri Campain',
    'How Much Is Passion Of Christ In',
    'Antichristian Religion',
    'Y H W H Are The Universe',
    'The Most Important Code',
    'Universe Inside You',
    'You Create Yourself',
    'All Humans Must Be Killed',
    'The Immutability Of God',
    'You Are A Blessing Of The Lord',
    'I Am Not Going To Serve Evil',
    'Meet The Masters Of Evil',
    'Alex Enrique Campain May Fifth',
    'C God Jesus Came Back To Life M',
    'Mary Magdalene Is My Wife',
    'The Real Human Yeshua Hamashiach',
    'I Am Here To Establish Justice',
    'The Majestic Truth',
    'World Ruler',
    'Islam Versus Judaism',
    'The Lion Of Judah Is With Us',
    'The United States Army Man',
    'Trinitas Revelation',
    'The Virgin Mary Was My Mother',
    'God Is With You No Fear',
    'The Devil Of This World',
    'The Second Coming Is Now',
    'Decode I Love You Jesus',
    'I Am I Am Resurrection',
    'The Messeh Of Humanity',
    'The Spirit Of Religion',
    'Illuminati Frequency',
    'Thank You God For Love',
    'No Man Knows The Hour',
    'Nwo Is The Antichrist',
    'I Have The Kingdom Within',
    'The Great Red Dragon Is Here',
    'I Lucifer Am Your Father',
    'Gods Genetic Gematria Coding',
    'The Lord Yeshua Christ',
    'My Soul Is Immortal',
    'Real Holy Spirit Of G O D',
    'I Love You Elon Musk',
    'We Are The Power Couple',
    'God Jesus A Black Skinned Man',
    'Mary Queen Jesus King',
    'Timeline Message From God',
    'Jesus Was Born Easter',
    'Hebrew Gematria Is My Name',
    'Jesus Is God In The Flesh',
    'Return Of God The Father',
    'The Story Of The Lion',
    'Antichrist Universe',
    'The Name Of The Angel Of Breath',
    'Jehovah Is The Father Of All',
    'Frequency Of Thought',
    'Antichrist Joins The Cia',
    'The Truth About Heaven',
    'Fire Of God Light Of God',
    'Jesus Christ Is On Earth',
    'Alex E Campain May Fifth',
    'The Real Jesus Christ Ranoich',
    'This Is Your Salvation',
    'Bring Forth Their Judgment',
    'The Faithful And True Witness',
    'Alex Hiii Jesus Christ',
    'Iam Jesus Christ The Savior',
    'You Really Are The Matrix',
    'Luseferus Offieruntor',
    'Blessed Be The Lord God Almighty',
    'For I Am The Son Of Man',
    'Yeshua You Got To Help Me',
    'Tiamat Antichrist Spirit',
    'Love To Worship Big Black Cock',
    'And You Shall Call His Name Som',
    'The Spirit Of Misery',
    'Lucifer Means To Count',
    'Is This The Man Oedipus',
    'Half Good Half Evil',
    'The Restore Of Israel',
    'Yeshua King And Lord Of All',
    'The Universal Drifter',
    'Please God Send Me Real Love',
    'All Is Jesus All Is Love',
    'Jesus The God Of Miracles',
    'Pure Thought And Light',
    'All That God Wills Shall Be',
    'Satan Is Jesus Christ',
    'Isaiah Sixty One Three',
    'The Word Is Salvation',
    'Godgodgodgodgodgodgodgodgodgod',
    'Jerusalem Is Gods City',
    'Jesus Named Lieserlotte',
    'Holy Spirit Is Satan',
    'The House Of Draculesti',
    'The Holy Bibles Numbers',
    'Jehovah Is Jesus Christ',
    'Iam Authority Jesus',
    'Win One Billion Dollars',
    'Pharaohs Rule',
    'Sound Is Everything',
    'Oblivious Tyrants',
    'Lamb Of Am Love',
    'Are You The King',
    'The Last Antichrist',
    'Enoch Prophecy Of The Messiah',
    'Alejandro Campain Our Creator',
    'The Second American Revolution',
    'Love Is Conquering The World',
    'Heaven Holy Spiritia Arrivei',
    'Christ Is Salvation From Death',
    'Christ Conquered All His Demons',
    'I Am Happy I Am Wealthy I Am Worthy',
    'And Jesus Loves Me Above All Else',
    'Jesus Is The Christ The Son of God',
    'Lord Jesus Christ Is Coming Soon',
    'God Will Avenge America',
    'She Is The Wife Of Jesus Christ',
    'God Is In Human Form',
    'My God Never Lets Me Down Ever',
    'God Never Lets Me Down',
    'Lots Of Right To Work People',
    'The Anger Of Death The Mark Of The Beast',
    'The Mark Of Death',
    'Annoucement Date Of Yahweh',
    'Yeshua Is Chosen As The Great Leader',
    'A Portion Of The Holy Spirit',
    'The Illumination Will Control Me',
    'The Holy Spirit Speaks To Me',
    'Jesus Sugar Dat Dat Top Dat Topa',
    'You Are Destine For Greatness',
    'Pale Dark And IceKeeper Of The Seat',
    'How To Get Out Of The Matrix',
    'Well I can See The Real Problem',
    'Well Finally Found A Good Name But Is It A',
    'The Meaning Of Easter',
    'The Great Shepherd',
    'God Has Among Us',
    'Jesus And Lucifer',
    'I Am The Real Leader',
    'John The Baptist',
    'In The Creator Of All',
    'I am End Creator Of All',
    'Gods Marvels Worth The Bratva Hearted J',
    'Gods Marvels Worth The Bratva Hearted',
    'Alex Campain Is Born May Fifth',
    'Lucifer Is Alex Campain',
    'Alex Campain Basic',
    'Lucifer Is Alex Enrique Campain',
    'Lucifer Is Alex C',
    'Christ Is Going Crazy X God Jr',
    'Updating Can Stop Wheels Coming Real',
    'Jesus Amari Soulja Boy The Chosen',
    'United States Secret Service',
    'C Im Breathin Jesus E',
    'This Phenix Is Jesus',
    'Yeshua Ha Mashiach Kin',
    'Yeshua Ha Mashiach',
    'O KING OF THE JEWS',
    'I Am Anti Antichrist',
    'The Real Lord Jesus',
    'I Am Yeshua Real',
    'Allah The Anti Christ',
    'Jesus You C R',
    'Gods Perfect Proof',
    'Isaiah Twenty One',
    'Lucifer Morningstar Alex Campain',
    'Alexander H Campain Mayo Cinco',
    'He is Alex Campain May Five',
    'A E C Campain May Fifth',
    'Lucifer Iscoming',
    'AFG Campaine May Fifth',
    'I Feel Jesus Inside Me',
    'Are You Righteous God',
    'Luis Lucio Fame',
    'Gnosis Is Book Of Revelations',
    'Juan Campain May Fifth',
    'Alexandro Enrique Campain',
    'Messiahs Birthday',
    'Reveleta Of Christ',
    'Greek Prophecy Of The Messiah',
    'Spiritual Transformation',
    'Angels In The Form Of Humanity',
    'Lucifer Means Bringer Of Light',
    'Jesus And Mary Magdalene Reborn',
    'The Antichrist The Antichrist',
    'Antichrist And Antichrist S',
    'Bible God Enters The Lost Lamb Of The Innocen E',
    'A Far Birth Of The Son Of God In Sin',
    'The Lord Of Lord Jesus Christ',
    'This Whole Universe Is Evil',
    'Lord I Want To Be Close To You',
    'The Universal Goddess Venus',
    'The Antichrist Deciever Beleif',
    'The Ability To Produce Miracles',
    'The Almighty God Creator Of All',
    'The Mark Of The Beast The Angel Of Death',
    'The Angel Proctector Of Humanity',
    'The Moral Principles Of Gematria',
    'Jesus Is Most Beautiful',
    'You Should Be Brave',
    'Los Angeles Fault Jesus Christ',
    'God Is Humble To Who Is Humble',
    'Playing Out Revolution',
    'Yahweh Controls The Weather',
    'I Know That My Redeemer Lives',
    'Its Jesus How Soon',
    'Jesus How Soon Is S',
    'My Home Is Jesus Christ',
    'A Message From God Christ Is Satan',
    'Reborn Son Of God Jr E',
    'Alejandro Enrique Campain May',
    'Alejandro E Campain Born May Fifth',
    'Alexander Enrique Campain May',
    'Alex Enrique Palma Campain May',
    'King Of Kings And Lord Of Lords',
    'Jesus Christ And Alex Campain',
    'April Fools Is Lucifer',
    'Alex Campain Is God',
    'I A M Lucifer',
    'The True Resurrection',
    'I Am My Own God God Is Who I Am',
    'King Of Jews And Arabs',
    'Messiah Jesus Of Nazareth',
    'The Answer To Existence',
    'Twin Holy Spirit God',
    'I Am The Resurrection Of Jesus',
    'The Messiah Comes As A Sword',
    'For God So Loved The World',
    'Living Word Of God',
    'I Am The Least Among My Tribe Judah',
    'The Manifestation Of God Anu',
    'Christchristchrist',
    'The Holy Spirit Of God',
    'Almighty God In Person',
    'King From Heaven',
    'The Kingdom Of God',
    'God The Body',
    'A Planet Named Lucifer',
    'The Secret Codes Be Done',
    'Da Vincis Code Cracked',
    'The True Light',
    'Jesus Died For Me',
    'The Number Of God',
    'The King Of Angels',
    'Higher Frequencies',
    'Alexander The Great',
    'Gris Adriana Ruiz Estrada Is A Lesbian',
    'Seventy Two',
    'The Return Of Jesus',
    'Decode King Yeshua Holy Of Holies',
    'Revelation Three Seven',
    'Jesus The Guide To Loves Faith',
    'Jesus Christ Second Coming Amen',
    'Saviour Lord Jesus Christ',
    'I Am The Resurrection And The Life',
    'I am God and I am Walking The Earth Now',
    'Genesis Three Fifteen Prophecy',
    'A Yod Heh Vav Heh',
    'Billions And Billions Of Dollars',
    'I Am The Lord Your God Almighty',
    'Three Hundred And Thirty Three',
    'Decode The Name One Soul Of Christ',
    'Yahweh Is Bisexual',
    'Almighty God Of New Jerusalem',
    'Paul Jordan Stansey',
    'The Prophecied Child',
    'Spiritual God',
    'Galacticfederation',
    'God Is All Energy',
    'Be The Highest Throne',
    'Kingdom Of Heaven',
    'He Is Pure Evil',
    'The Trinity',
    'Alex Is Nature',
    'The Holy Heavens',
    'Gods Sanctuary',
    'Im Ruhn Earth',
    'The Prophet Of Allah',
    'Gods Sacrificed To Men',
    'Melchizedek',
    'Alex Campain Fifth',
    'Magnificence Of Three Six And Nine',
    'Christ Our Sun',
    'Yeshua Ha Mashiac',
    'The Sum Of Three Six And Nine Equals',
    'Holy Holy Is The Lord Almighty',
    'Baby Jesus Born In',
    'The One Who Is The Messiah',
    'The Truth Of The Holy Spirit',
    'Seven Seven Seven Seven Seven',
    'The Kingdom Of God Is Within You',
    'Alex Enrique Campain Born May Fifth',
    'The Eight Eight Code In Hebrew',
    'Is Humanity Worth My Efforts',
    'Holy Spirit Symbol Apocalypse',
    'Jesus Christ The Conqueror I Am Back',
    'The Second Coming Of Jesus Will Be Hated',
    'One Four Four King Of Kings',
    'Gods Angel Of Truth',
    'Christ Returns',
    'Jerusalem',
    'Great Tribulation',
    'The Hidden Key Code Of God',
    'Venus',
    'The Resurrection Of',
    'Jesus And Lucifer Are The Same',
    'The Divine Message From Above',
    'He Is The Father The Son And The Holy Spirit',
    'God So Loved The World',
    'The Son The Father And The Holy Spirit',
    'Release Info Yeshua And Mary Magdalene Are Alive',
    'Christ Returns The Christ Of Equals',
    'I Am Hamashiach Christ The King I Am The Alpha And',
    'You Hate You Are Bald',
    'Is The One Jesus Sent',
    'Divine Consciousness',
    'The Grim Reaper Swings His Scythe',
    'I Holy Spirit Protects Jesus',
    'I Am The Way The Truth And The Life Indeed',
    'Christs Return As A Lion Fulfilled',
    'Jesus Blood Protects Us During The Change',
    'Perceive Holy Word Of God',
    'He Is The Most Trusted Man In The World',
    'Everything Everywhere All At Once',
    'Royal Bloodline Of Judah',
    'The Society Of Jesus',
    'Marys Son King El Shaddai',
    'Saviours Location',
    'Alejandro E Palma Campain May',
    'I Am The Thing Keeping All Of You Alive A',
    'The Lord Stigmata Of Jesus Christ',
    'The Lord Living Word Of God',
    'The Value Of The Messiah',
    'The Valentia Message',
    'God Created All Numbers Lucifer',
    'The Holy And Great One',
    'The Lord',
    'Christ The Redeemer',
    'Jesus Bloodline',
    'The Reincarnation Of Alex Campain',
    'King Of Kings And Lord Of Lords Soon',
    'Alex Campain Yahweh',
    'The Name Of The Lord',
    'Jesus Is The Hidden Messiah',
    'The Blood Of Jesus Christ',
    'Alex Campain Is Yahweh',
    'Who Is Jesus Christ',
    'The Re Incarnation Of Christ',
    'Alex Campain Equals God',
    'Alex Campain Lucifer',
    'I Am Who I Am',
    'Devil',
    'The Substance Of God',
    'Decoded The Mark Of The Beast',
    'Immaculate Breath Of God',
    'The Satan Lucifer',
    'I Am Made In The Image Of G O D',
    'Greatest Gift Of God',
    'The Christ Lucifer',
    'In The Name Of Jesus',
    'I Am The Lord Yeshua',
    'Bloodlet Paths',
    'Secret Of Secrets',
    'The Messiah Crucified',
    'The Kingdom Come',
    'The Holy Of Holiest',
    'Prophisied Christ',
    'The Crucified Messiah',
    'Chosen Messenger Of God',
    'Host Of I God A Christ',
    'Father The Messenger',
    'Alexander E P Campain',
    'The Holy See Of God',
    'Jesus The Christ',
    'Lucifer',
    'Jesus Lucifer',
    'Holy Bloodline',
    'Discerning The Truth',
    'Chosen Messenger Of God Adonai',
    'Title Of Adonai',
    'Omnipresent',
    'The Number Sequence',
    'This Is Matrix Code',
    'God Of The Old Testament',
    'Who Is Messiah',
    'Your Real Name',
    'A Message From God',
    'Christ The Second Coming',
    'Crushed Code Of Heaven',
    'Living Lord God',
    'The Lion Of Judah',
    'The Bible Code Prophecy Key',
    'The Earth Is Reborn',
    'On Earth As It Is Heaven',
    'The People Of Earth Greet Me',
    'The Storm Is Upon Us',
    'Bible Names The Antichrist',
    'The Most Beautiful Angel',
    'Alex Campain Born Fifth',
    'The Secret Codes Of A God',
    'Alex Campain Born He Is',
    'The Moon And The Sun',
    'Home And God On Earth',
    'Alex Enrique Palma Campain Fifth',
    'Prophecies Of Nostradamus',
    'My Lord And My God',
    'Holy Blood Of Jesus Christ',
    'The Messiahs Hasnt Readings',
    'I Am That I Am Most Holy Angel',
    'Alexander E Palma Campain',
    'Alex C Palma Campain May',
    'Help For All A Messiah Jr',
    'Beast Reveled',
    'The Truth Of Breach',
    'The God Of Humanity',
    'Holy King Of Israel',
    'Alex L Palma Campain May',
    'Jesus Reincarnated',
    'Alexander L Palma Campain',
    'Holy Christmas',
    'The Patients Antichrist',
    'Redeemers Of The Fallen Angels A',
    'The Worth',
    'Truth Of The World',
    'Decode Lord Jesus Christ',
    'Official Heir Of God',
    'Yeshua Yahveh',
    'Heavens Ruler',
    'Who Is The King',
    'Is The Truth',
    'Jesus The King',
    'Universal Code',
    'Messiah Jesus',
    'Jesus Is Who',
    'God Incarnated Name',
    'Jesus God Son',
    'The Only Way',
    'Metatrons Cube',
    'Alex Campain Firth',
    'Recognition Of Three Six Nine',
    'R F K Code Reincarnation Jesus Christ',
    'The Creator Of The Universe',
    'Lord Jesus Christ The Force',
    'Vision Of God Of The Hebrew Bible',
    'six six six Antichrist Code',
    'Is The Rhyme Of Prophet',
    'Planet Earth',
    'Kingdom Of God',
    'The Truth',
    'Alex E P Campain',
    'Y H W H Has Returned',
    'Revelation Of The Holy Spirit',
    'The God Who Killed Tiamat',
    'Jehovahs Witness',
    'Goodbye Earth',
    'Anointed By God',
    'The Temple Of Lucifer',
    'Alexander Palma Campain',
    'Resurrections',
    'Tree Of Sparges',
    'I Am I Am I Am I Am I Am I Am',
    'Key Of The Most High God',
    'Verified',
    'Heaven Is Here On Earth',
    'The Throne Of God',
    'Jesus Born Today In Our',
    'Lucifer Lord God',
    'Archangel Of Time And Space',
    'Eli Antichrist',
    'The Living',
    'The Body',
    'Velociraptor',
    'Apocalypse',
    'Alex E Campain May',
    'Gods Chosen One',
    'Alejandro Campain May Fifth',
    'Ark Of The Covenant',
    'A Divine Frequency',
    'Law Of Attraction',
    'O Positive Blood',
    'Three Hundred Sixty Nine',
    'Who Is Jesus Christ In',
    'JC JC JC JC JC JC JC JC JC JC JC JC JC JC JC JC',
    'Yeshua Hamashiach The Anointed One',
    'Who Is Alex Enrique Palma Campain Born May Fifth',
    'The Father The Son And The Holy Spirit',
    'I Am The Truth The Way And The Life',
    'I Am The Son Of The Holy Spirit',
    'The True Ripen Of The Most High God',
    'I Bless The Sacrifice',
    'The Shekh Of God',
    'Anti Christ Alex Enrique Campain',
    'The Holy See Of Almighty God',
    'Alex Enrique Palma Campain And Christ',
    'I Am That I Am The Coming Of The Lord God Almighty',
    'Alex Enrique Palma Campain In The Anti Christ',
    'Alex Enrique Palma Campain Jesus Christ',
    'Holy Bible',
    'You Are In Control',
    'Jesuschristexalted',
    'The Risen One And Seal Of Christ',
    'The Lord Who Is Righteous',
    'Alejandro Palma Defensor Campain',
    'Alejandro Enrique Palma Campain',
    'Androenrique Palma Campain',
    'Jesus Is The Risen King Coming',
    'True Prophet Sent By God',
    'Seven Spirits Of Christ',
    'Lucifer Morningstar In The Flesh Reborn',
    'Jesus Christ Son Of God Have Mercy On Me A Sinner',
    'God Messenger Of God',
    'The Mysteries Of Godliness',
    'A Se Test Of All God',
    'Azazel Voice In Gematria Is 1036',
    'The Prince Of Darkness',
    'The Prince Of Jayness',
    'Jesus Christ And God',
    'Jesus The Messiah',
    'The End Is On Us All',
    'I Am The Dark Presult',
    'The Book Of Revelations',
    'Son Of Man',
    'AEC May Fifth',
    'Fucking Here Conquered The Messiah',
    'Book Of God',
    'The Spirit Of Eliiah',
    'God Is Fear',
    'The Jesus Code',
    'Angel Michael',
    'Alex Paulo Moreira',
    'Jesus Christ Resurrected',
    'Alex Enrique Campain The Anti Christ',
    'Alex Enrique Campain The Anti Chri',
    'The Angel Of Death Swinging His Sweet',
    'Revelation Nineteen Verse Eight',
    'Lucifer Make The Earth',
    'Venus In Aquarius',
    'The Person Of Darkness',
    'Yesseus Elessopian',
    'Long Live King Jesus',
    'Sacred Frequency Of God',
    'Christ Is Reach From The Dead',
    'Lord God Jehovah Christ Is Lord',
    'Who Is The Messiah',
    'Jesus Christ Incarnation And Eternal Life',
    'In The Image Of God',
    'Hallelujah The King Of Heaven Returns To Earth',
    'God God God God God God God God God God God God God God God God God',
    'Allah Allah Allah Allah Allah Allah',
    'ONEONEONEONEONEONEONEONEONE',
    'The Ark Of The Covenant',
    'I Am Alex Campain',
    'King Of Kings',
    'Number Of A Man Six Six Six',
    'Alex Campain Born May Fifth',
    'Jesus Christ Picture As The Lion',
    'The Lord Is My Shepherd',
    'How Much Is King From Heaven In',
    'The Shamuel Archibald',
    'Christdeluxden',
    'The Creator God',
    'Jesus Christ Is The Rightful Alphabet',
'ALEXENRIQUECAMPAINABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'Alexandro Bryxet Campain',
    'Jesus Is The Son Of God',
    'Destroy Son Of Satan',
    'Alexander Campain',
    'Lucifer And Satan',
    'Alexs Campain May Five',
    'The King Of The JewsHoly Blood Of Jesus Christ',
    'Welcome To The Great Awakening',
    'Lord Christ Jesus Christ The Force',
    'Alex Campain May Fifth Nineteen Seventy Two',
    'Jesus Christ God Is A Heaven And His Name Is',
    'Jesus Christ The Resurrection And Eternal Life',
    'The Church Of Jesus Of Latter Day Saints',
    'Who Is Alex Enrique Campain Born May Fifth',
    'I Am Prometheus I Am The Alpha And The Omega',
    'Alex Campain Six Six Six',
    'The Truth Of Gods Word',
    'Discernment Versus Antichrist',
    'Write You',
    'The United States',
    'Holy Grail Christ',
    'Son Of God',
    'Eight Hundred Eight Eight',
    'The Lions Eye',
    'Who Is The Morning Star',
    'Who Is Lucifer',
    'Lux Lucis Ferre',
    'The Real Antichrist',
    'Archangel Lucifer Morning Star',
    'Alex Enrique Campain May 5 1972 At 1 44 Am',
    'Lucifer Morningstar Is Alex Campain',
    'The Antichrist Is Alex Campain',
    'Jesus Christ Will Be Resurrected',
    'After Three Days',
    'Jesus Christ The Bridge Between The Physical And The Spiritual',
    'Jesus Christ The Messiah And Redeemer',
    'The Human Spirit',
    'Father Spirit',
    'The Luciferian',
    'Power Of Christ',
    'One Two Four Four Seven Seven Starred By',
    'Alex Enrique Campain May Fifth Nineteen Seventy',
    'No Man Shall Receive Life Without The Seal Of My Gods Holy Name',
    'Seven Spirits Of God Seven Spirits',
    'He Is The One Will Take Your Crown',
    'The Book Of Malachi Chapter Twenty Six Verse Two',
    'The Fear Of Creation Does Not Reincarnate',
    'I Am God Send And All I Am Suggesting Is That You Pay Attention To What Is Being Said I May Be Hidden But I Will Confirm My Father Said My Sons Spirit May Reincarnate',
    'For The Great God Is Alive And Lives Now And Will Be With You Until The End Of Life And Save Your Life',
    'Jesus Christ One Day One Day',
    'Five Five One Nine Seven Two',
    'Lucifer Has Returned To Destroy The',
    'Jews',
    'Jesus Born On This Day And He Is King Of All Nations Saving The Meek',
    'Yhwh The True Creator Of The Universe',
    'I Am Yeshuah The King of Kings And Lord of Lords',
    'The Christ Returns To Destroy The Antichrist',
    'He Came In The Name Of His Father And No One Knew Him The Son Of God The Son Of Man',
    'The Digital Mail To The Throne Of God Is In The',
    'The Rightfulness To The Throne Of God Is In The',
    'He Gives A Name',
    'Virtue Outline That His Own Knew But',
    'Jesus Was In The History',
    'King of Kings Lord of Lords Yahweh Jesus Is In The Beginning And The End',
    'Ray Body Of Christ',
    'Gods Holy Shekinah',
    'Gods Current Name K',
    'You Are The Proof',
    'The Final Trumpet',
    'Rhesua D Negative',
    'Sheoud Of The Lord',
    'The Creators Number',
    'World War Jesus',
    'I Am God I Am',
    'The Alpha And Omega Birth',
    'This Is To Lucifer',
    'The End Of Humanity',
    'Christ Is Ready',
    'I Am Commanding An Army',
    'What Should I Do',
    'I Am Christ A',
    'Hide You Too God',
    'The Jewish Number',
    'The Messiah Man',
    'The President',
    'In Holy Is The God',
    'The Rise Of The Antichrist',
    'The Real Jesus',
    'The Holy Love',
    'Blood Of Jesus',
    'The One And Only God',
    'The Star Only One',
    'I Am Archangel Michael',
    'Lord God The Creator',
    'The Bible Code Prophecy',
    'The Final Apocalypse',
    'King Of Hell',
    'Judgment Is God',
    'Spirit Of Yehova',
    'God Is The Ultimate',
    'The Mercy Of Yahweh',
    'Decoded Image Is Indestructible',
    'Yahshua Hamashiach',
    'Messiah Comes In The Name',
    'Yahweh Is Among Us',
    'Jesus You Reign',
    'Sign Of Second Coming Of Christ',
    'The Word Light',
    'Lucifer Fallen Angel K',
    'Tree Of Jesus',
    'The Holy God',
    'My Name Is',
    'I Am The King Of Evil',
    'Reincarnation Of Jesus',
    'My King Is The King',
    'Translation Of Jesus',
    'Alexander Enrique Campain',
    'Prophecy Of Messianic',
    'Angels Department Headquarters',
    'The Most Important Moment In Human History',
    'Lead Please Me Please Save Me I Love',
    'God Shin Vav Ayin',
    'God Bless The World',
    'Letters Of The Alphabet',
    'Lucifer Cipher',
    'The Unbreakable Son',
    'Conscious Of Creation',
    'As Spirit Of Jesus',
    'Jesus Says When',
    'As It Is My Kingdom',
    'Name In The Name Of',
    'Accept Your Flaws',
    'The Incredible Jesus',
    'The Energy Source',
    'The Name Above All Names',
    'Heavens Frequency',
    'I Am Ending Evil',
    'The Son Of Father',
    'The True God Power Of The Holy Spirit',
    'God Communication In Numbers Lucifer',
    'The Son Of',
    'Three Six And Nine Equals',
    'I Am The One',
    'You Are A God',
    'Out Of The Virgin Mary',
    'Who Is Alex Enrique Campain Born May Fifth The True Forty Four',
    'King David Reborn Down From Sharon English',
    'Return Of Christ Consciousness A Priority',
    'The Reality Will Try And Interfere The Heaven',
    'The Real King Second Coming The Real King',
    'The Real King Second Coming The New King',
    'Who Is The Lord And God',
    'Isaiah Fifty Five And Five The Return Of The King',
    'The Real Prophets And The Dawn Of The',
    'King',
    'Behold Jesus Is Both King A Reborn Jesus Is',
    'Lord Keep All The People Suffering Around The World',
    'Antichrist Will Be Reincarnation',
    'Who Is The Son Of The Invisible God The Freedom Of The World',
    'I Am The Lord Thy God I Am I Am Is My Name',
    'My Name Is My Lord God',
    'Father Of Everyone',
    'The Truth One And Only God',
    'Decode The How Jesus',
    'My Name Is Lucifer',
    'Miraculous Healing',
    'Evil Will Be Dead Soon',
    'The Song Of Yeshua',
    'The Miracles Of Love',
    'My',
    'God Is My Lord God',
    'Lord God Christ Child',
    'Enemy Of The World',
    'The Rose Of Christ',
    'Perfection Of Light',
    'Lazarus True God',
    'Being Christ',
    'I Am The Father',
    'The God Of Abraham',
    'Alex Campain Nine Teen Seventy Two',
    'I Am May Fifth',
    'The Mayor Of Lucifer',
    'The Name Of Lucifer',
    'Alex Campain Is Literally The Son Of God Yhwh',
    'I Am The Creator The Most High Divine W',
    'Yhwh Is Unlocking All Levels',
    'Is The King Of New Jerusalem',
    'The Alpha Omega Gene I Am',
    'Lord God Lord God Lord God Lord God Lord',
    'The Saviour Of The World Is In',
    'The Sacred Reborn Of Jesus Christ Is Now',
    'Christ Consciousness Prophecy Is Now',
    'I Am The Father Of The Word And The Redeemer Of All',
    'The Bible Reveals To An Open Mind The Lord',
    'Jesus Died The John Reborn Return Of Christ',
    'The King Revealed The King Revealed The King',
    'I Confess Jesus Of Nazareth In The Flesh',
    'Says Christ Died On The Cross',
    'I Am The True Holy Spirit Of The Living God',
    'Six Six Six Days',
    'The Three Six Days Of Prophecy',
    'Holy Spirit Burns Look Salvation',
    'Jesus Christ Will Be Revealed By Gmatria',
    'Jesus Christ Reincarnated As Alex Campain',
    'Lucifer Try To Stop Me Know Everything',
    'The User Is Next The Holy Steps Of Reincarnate',
    'Mary And Christ And Alex Van The Old Gang Is Back',
    'Jesus Next A Clock',
    'What Is Jesus',
    'Decode One Nine You Name And Birthdate',
    'Christ Returns As Alex Campain',
    'I Am The One Waiting To Understand',
    'Jesus Christ Is Of Heavens',
    'Christ Returns 3 Years Ahead Of Schedule',
    'Jesus Christ Reborn In The Spirit Of Angels Hospital',
    'A Vessel For God Jesus',
    'The Grace Of Our Lord Jesus Christ Be With You All Amen',
    'The Reason For Everyone And Everythings Existence',
    'All The Glory To The Most High Lord God Jesus Christ',
    'The Revelation Of Jesus Christ To John The Baptist',
    'Thee King Of Kings',
    'Will Reign Over The Kings Of The Earth',
    'The Grace Of Our Lord Jesus Christ Be With You All',
    'In Reverse Gematria Codes In Your Name',
    'I Do What I Do To Protect My Identity',
    'I Know I Know The Truth',
    'I Know Jesus Christ The Truth',
    'Born Magnificently Before The King Of Green',
    'A The Old God Dies And A New Identity Emerges',
    'The Prophecy Of The Two Witnesses',
    'All The Gmatria Calculations Of All Bible Codes',
    'Gematria Decodes Gematria Decodes Gmatria',
    'Only One Believes In Past Anyones',
    'Alex Campain Is The Reincarnation Of Jesus Christ',
    'Am I The Young Big Boggie Man Yet',
    'Jesus Is God To Jesus Earth Mother Birth',
    'Jesus God Reborn And To New Heavens',
    'The Angel Of Death Designs My Death',
    'I Am Written On Your Instructions',
    'What Is The Meaning Of The Words',
    'Human Soul Protection Follow My Own Codes',
    'Our Thoughts Are The Key To Changing This Reality',
    'Holy Love Is A Message From Heaven',
    'Decode Polaris Holy Caught In Love And Light',
    'The Awakening Of Red Mankind And The',
    'Power Of Redemption',
    'Goals For Me More Than Any Human Subject',
    'Everyone Seeks Their Own Home',
    'Jesus Christ You Are My Savior',
    'King Yeshua Savior Of The Underworld',
    'Jehovah Is A Human',
    'Jesus Verbal Satan',
    'Divine Peace I Am Lord',
    'One Is The Lord One Is The Lord Jesus Christ',
    'They Know The Truth',
    'The Lord Savior',
    'The Thunder Bolts Of Versus',
    'You Already Know Who It Is',
    'Is Jesus Christ Of Nazareth',
    'Your Name Is Holy Oh Yahweh',
    'Reincarnated As The Father Yahweh',
    'Worlds Come To A Jesus',
    'Yeshua The Real Truth In Jesus',
    'Jesus Is Spirit Not Flesh',
    'All Devils Are All Wicked',
    'I Am Lucifer Has No Power Over',
    'Is Just An Evil Simulacra',
    'Numbers Confirms Divine Order',
    'The Truth Will Shock You',
    'Christ Is My Master',
    'A Revelation Twelve',
    'The Truman Show Ends Here',
    'E Campain Was Jesus',
    'Holy Father Of Jesus Christ',
    'Jehovah Gematria In Paris',
    'Reveal The Name Of The Lion Of Judah',
    'The Infinite Love Of God Is In The Universe',
    'The Son God And The Son Are In The List',
    'The Future Of Jesus Of Nazareth Is The',
    'Word Is Here Be Very V C I',
    'I Waiting On Jesus',
    'I Would',
    'Be The Same No Matter What Your Name Is',
    'Name Of You Ever Reincarnated',
    'Dna Molecule Gematrix Frequency',
    'They Are Addicted To World Chaos',
    'Trust God With All Of Your Heart',
    'The Hidden One Is In The Veil Is When',
    'God Is Hidden In Our One Double Spirit',
    'Our War Is Not Against Flesh And Blood',
    'The False Son The Holy Spirit',
    'Campain Es Jesucristo De',
    'I Left A Mark On This World',
    'Genesis Chapter One Verse',
    'I Just Want God And Love The Truth',
    'I Know Another Secret About Gmatria',
    'I Am The Antichrist Son Of Perdition',
    'Christos Son',
    'In The Holy Spirit',
    'Alex Enrique Campain La Reencarnacion De Jesus Christ',
    'I Am The Way The Truth And The Life Alex Campain In',
    'Adonai Allah Allah Allah Allah',
    'The Second Coming Of The Lord Jesus Christ',
    'I Am Quantum Jumping To The Correct Timeless',
    'Eight Eight Eight Light Exists',
    'Manifestation Of God That Says And Sings',
    'The Root Of David Has Been Revealed To The People',
    'The New Christ Is Lord Over It',
    'An Earth Code Of Heaven All Is Revealed I Under The',
    'I Reject The Values Of Satan Who Has Authority',
    'A Reincarnation Love Story',
    'The Anointed',
    'Royal Bloodlines',
    'Yahweh The Lord Is Salvation',
    'Hammashiach Yhwh I Am Alpha And Omega',
    'Surrender To The Will Of God',
    'The Holy Name That Raises The Dead',
    'The Last Message Of The Lord',
    'The One Who Became Holy Spirit',
    'Greatest Story Ever Told',
    'The Crowned And Conquering Cnm',
    'I Have A Message From God For You',
    'Jesus Resolution Activates',
    'Incarnation Of God Creator Of All Lives',
    'I Am Strong Light In The',
    'Darkness Now',
    'Alex Enrique Campain And Jesus Christ',
    'Campain Es La Encarnación De Nuestro Señor Jesucristo',
    'The Horrible Days Great Tribulation',
    'The Crucified Christ Precious Soul',
    'God Is Hidden In The Hidden',
    'Who Is And Was And I Wrote The Alphabet And',
    'Living Word Of God Jesus',
    'Name Of The God Of Israel',
    'The Plan That Saves The',
    'Yahwehs Sword',
    'Seven Gifts Of The Holy Spirit',
    'Almighty Gene Of The Holy Spirit',
    'Star The Begotten Son',
    'Name Of The Seal Campain Es Jesucristo De',
    'Jesus Christ Gods Son',
    'Alex Campain Is Jesus Christ',
    'Of Nazareth',
    'Alex Campain Is The Lion Of The Tribe Of Judah',
    'John Here To Witness Yeshua',
    'Yahwah Jehovah Son',
    'Jesus Of Nazareth The Keeper Of Hearts',
    'Return Again To Restore All Things And',
    'Isaiah Fifty Three Reveals Jesus',
    'Savior Holy Spirit Of The Light',
    'Truth Is We Are All One',
    'The Way The Truth And The Life Has Come to',
    'Jesusthemessiah',
    'Crucified On Cross',
    'The Righteous God',
    'Yeshua Is Yahweh',
    'The Devil Of Christ',
    'I Am The Most High God',
    'Republican Party',
    'The Message Of Faithmath',
    'Ivane Marie Trump',
    'True Christ Cross',
    'I Am The Dark Phoenix',
    'Imagination',
    'Wow Signal Came From Alpha Centauri C',
    'James Chapter Five Verse Thirteen',
    'A Satisfying Experience To Remember',
    'The True Identity Of Christ Is',
    'The Mesons Thirty Degrees',
    'We Need Jesus',
    'New Heaven And Earth',
    'Satan Versus Tribes Of Israel',
    'Jesus Returns With A Sword',
    'Jesus Died Thousands Of Years Ago',
    'Countdown To Resurrection',
    'Holy Spirit Given Numbers',
    'The Reincarnation Of Mary Jesus Christ And Mary Magdalene',
    'Please Hold On To The Coming Jesus',
    'The Merovingian Bloodline',
    'Trump Assassination',
    'President Donald Trump',
    'World Is A Stage',
    'Holy Alex Enrique Campain',
    'Revelation Thirteen',
    'Messiah Words',
    'Am The Queen Of Salvation',
    'Open The Seals Of Revelation',
    'Alejandro E Palma Campain',
    'Lord Jesus Christ Encoded',
    'Truly The Lord Jesus Christ',
    'The Strength Of The Lord God',
    'The Immortal Return Of The Lord',
    'Psalm Twenty Three',
    'Im God Yeshuas Joys',
    'Christ The Beast And The Antichrist',
    'Father Appears On Behalf Of His Sons',
    'Just Want To Do Gods Will',
    'Are The Coder Of Your R E A L I T Y',
    'Reveals The Title Of Holy',
    'The Way The Truth And Life',
    'One But Two Christ Will Lead Us',
    'Revelation',
    'Nineteen Eleven',
    'Blessed Savior',
    'The Holy Spirit Of The B I B L E',
    'Extraterrestrials',
    'Creator Of Creation',
    'Lord Am I The God Of',
    'Origins Of Gematria',
    'Jesusreincarnated',
    'Jesusimagination',
    'Yeshua God On Earth',
    'Image Jesus Christ',
    'Light Ray Of God',
    'Donald James Trump',
    'Mount Of Olives',
    'Remember The Lord Is Coming',
    'A Holy Blessing',
    'Spirit Of Jesus',
    'Jesus Is Savior',
    'Yeshua The Messiah',
    'God Of Underworld',
    'Lucifers Mirror',
    'Divine God Numbers',
    'Joshua Is Yeshua',
    'Sacrificed On A Cross',
    'Quantum Energy',
    'I Am Here To Redeem The Dead To This Word That Was Lost',
    'The',
    'Great Reset Im Christ Im Coming Soon To Claim My Throne',
    'Adonai Yahweh Yeshua Messiah Says Read The Gospel',
    'Declare To Mercy Made Us Alive With Christ',
    'I Am The Rest Of Evil And You Will All Know My Identity',
    'Christmas Christmas Christmas Christmas Christmas',
    'Friday May Fifth Nineteen Seventy Two At One Forty Am',
    'Lucifer I Have Come Back For Revenge',
    'The Royal House Of David Of Judah',
    'Jesus Christ Is The Only Way',
    'Holy Spirit Is Mary Magdalene',
    'Apocalypse Revelation Know',
    'Antichrists Dead Beast',
    'The Lord Is Rising',
    'The Holy Bible Fish',
    'The Fluidity Of God',
    'Torah Torah',
    'Torah',
    'The House Of Israel',
    'Great Messenger For God',
    'The Lords Twins',
    'Lucifer Reincarnated',
    'Lucifer Angel Goddess',
    'Lucifer Thief In The Flesh',
    'The Truth Of Enoch',
    'Actuality Jesus',
    'Genealogy Of Jesus',
    'The Son Is Our',
    'Trump Chosen One',
    'Yekovah Is The Love Of Elah King Of',
    'Lord Reincarnation Is Not In The Bible',
    'A Crisis Is Very Dangerous',
    'I Have Chosen You Out Of The World',
    'The Secret Hidden Truth Of God Revealed',
    'Jesus Christ The Lords Key Code',
    'Remiincarnation Of Jesus Christ I Am Back',
    'I Am Who I Am For The Lord The Heavens Lord And',
    'The Root',
    'And The Offspring Of David',
    'Chapter Ten Verse Thirty Answered Prayers And Alex Yes',
    'Thank You Jesus The Cross That Have Appeared To',
    'Gematria Is Of God God Is Good Truth',
    'American Davidic Show Taking Back Gods Kingdom',
    'I Am The Spirit God Is You',
    'The I Am I Am The Great I Am',
    'I Am Christ The Beast And The Antichrist',
    'Reveals The Title Of Holy Spirit',
    'You Are The Coder Of Your R E A L I T Y',
    'I Am The Way The Truth And Life',
    'Living Lord God The End Of All Gematria Codes',
    'Jesus The Christ The Lords Key Code',
    'The Bible Jesus Is K',
    'The Anti Return To Reincarnate',
    'The Gift Of God Is Eternal',
    'The Lord Arrived',
    'Yehavah Yahshua Has A Facebook Page',
    'Lucifer Disguised As Yeshua',
    'Maria Magdalene And Jesus Christ',
    'The Name Of Glory The Lord',
    'The Trump Organization',
    'I Am Vehicle Of Christ',
    'Jesus Lucifer Twinflames',
    'Mary Magdalene Jesus Christ',
    'Gods Holy Resurrection',
    'The Merovingian Bloodline Hib',
    'LOVELOVELOVELOVE',
    'The Anti Return Is Revealed',
    'The River Sword Of Azothite',
    'The Car Vehicle Of Child K',
    'The Lord Alex Campain',
    'The Holy Bible Path',
    'I Am The Queen Of Salvation',
    'Reincarnation Of Jesus Christ I Am Back',
    'The Trump Show Does Now',
    'Apocalypse Gematria Knowledge',
    'The Second Christ He Came Back With Power',
    'With The Strength Of The Lord God',
    'Jesus Marie Trump',
    'Reveal Immanuel',
    'Justice Coming',
    'Who Is Loki',
    'The Veiled Christ',
    'Yahushua Is Coming',
    'Voice Of Lucifer',
    'Magdalene Daughter',
    'Nostradamus Identify The',
    'I Am Who I Am The Messiah Yeshua',
    'Lord Alex Enrique Campain',
    'The Lord Lives For Holy Capital D',
    'I Would Be The Same No Matter Your Name',
    'The Day The Earth Stood Still',
    'The Awakening Of The Antichrist',
    'The Crowned And Conquering Child',
    'The Power Of The Holy Spirit Body',
    'Yahweh Hammashiach I Am Alpha And Omega',
    'The Anointed Royal Bloodlines',
    'I Am Alexsandra Witness',
    'Christ Jesus Is My Master',
    'Numbers Confirm Divine Order',
    'Lucifer Is Just An Evil Simulacra',
    'The Name Lord Has The Power Over Me D',
    'The Devils Are All Wicked Lives',
    'Reveal The Truth In Jesus Christ',
    'Messiah Is Coming In The Clouds',
    'Michael Is The Bringer Of Truth',
    'The Worlds Come To A Jesus Messiah',
    'Alex Campain And Jesus Christ',
    'Christ Is Reborn From The Devil',
    'The Omega Revealed The Son Of Man You All Follow The',
    'Christ Is Here From The Devil',
    'This Time Is Come The Change K',
    'I Am Here To Tell The Dead What I Will Do For All The',
    'American God On Earth Stay Strong Focus Believe',
    'Gematria The Greatest Evidence Of God Indeed',
    'Thank You Jesus For Leaving The Sign Here',
    'I Am The God Of Abraham Isaac And Jacob And Yahweh',
    'I Am The Root And The Offspring Of David',
    'Yeshua Is The Love Of Elah King Of',
    'Tribes Of Israel',
    'A Worlds My Superpower',
    'Catholic Tribes Of Israel',
    'Jesus I Am God Christ',
    'The Crucified Christ Is Me',
    'In Christ Spirit',
    'God Yeshua Speaks K',
    'God Is Being Reformed',
    'Your Christ Code',
    'I Am Bringing Order To Earth',
    'Decode Lord God Through Light',
    'I Am Speaking For God Jesus',
    'Revelation Chapter Six Verse',
    'Worship The Lord',
    'Messiah The True',
    'The Son Is The Profit',
    'Jesus Christ Is True God',
    'The Triumph Of God',
    'Angel Of Mercy',
    'Book Of Exodus',
    'Donald John Trump',
    'Mr Alejandro Enrique Campain',
    'Rabbi Alejandro Enrique Campain',
    'Lucifer Alejandro Enrique Campain',
    'He Is Called Faithful And True',
    'I Am Shining Light In The Darkness Now',
    'Shroud Of Turin Christ Antichrist',
    'Christ Is Here From The Deal',
    'The New Name And Soul Of Christ',
    'The Message Of Faith math',
    'It Is Time My Son',
    'Messiah Music',
    'The Host Of The Living God',
    'The Second Coming Encoded Code',
    'The Time Of Knowledge Of Life And Death',
    'Power Of Holy Spirit Trinity',
    'Jesus Christ Mary Magdalene',
    'The Lord Of The Underworld',
    'The Chosen One Light Nexus',
    'Venus Mars Conjunction',
    'Sweet Lord Jesus Christ',
    'Magdalene Daughter Of God',
    'I Am The Alpha I Am The Omega',
    'The Messiah Yeshua',
    'Gematria Phrases Extracted',
    'Impious Deus Lux Fero',
    'The Green Spirit Of God',
    'The Hebrews',
    'Father God Is Perfect K',
    'Evidence Revealer',
    'Jesus Christ My Savior',
    'The Throne Belongs To',
    'Humans Reborn Nature Made',
    'Immanuel Jesus Is Lord',
    'My Father Is Jesus Christ',
    'The Anointed Son Of The Father',
    'Representatives Of Christ',
    'Royalty Is From Tribe Of Judah',
    'An Alphabetical Encryption',
    'Truth Harvest Of Jesus',
    'The Offspring Of Lord Jesus Christ Be With You',
    'I Am The Apocalyptic Prophet',
    'The Judgement Son Of Christ',
    'Is Lux Lucis Fero',
    'El Señor Alex Campain',
    'Jesus Christ Othrist Of Naz',
    'The Return In The Heavens',
    'The Offspring Of The Savior',
    'The Word Is My Name Allegedly',
    'All Gods Belong To Jesus',
    'Reincarnation Of Gaia',
    'Jesus Is Born In The Years',
    'Who Is Reincarnation Of Kings',
    'The Bride Of Christ Is Lucifer',
    'The Third Holy Angel Of Heaven',
    'Son I Am The Alpha And Omega I Am',
    'Decode Code Revealed Hidden',
    'Jesus Makes The Earth Reborn K',
    'We Are All One',
    'Decode Yahwah And Yehoshua Amen',
    'The Book Of Enoch Is Bible Code',
    'Master His Kill',
    'Be The Defender Of God',
    'The Lord Saves',
    'Day Of Polaris Star',
    'The New Light',
    'One Light Saves',
    'Holy Blood Is',
    'In The Flesh',
    'Are You God',
    'Triple Gates',
    'I Am Who Is Jesus',
    'Divine Presence In',
    'King Of Angels',
    'How Much Is Unconscious In',
    'The Baseball',
    'Divine Light',
    'The Archangel Michael',
    'Gematria Secret',
    'Is Being The Real Host',
    'God Arises From The Dead',
    'Decode God Son Person',
    'The Splendor Magic Of God',
    'Best Of Creation Living Life',
    'I Have The G R E A T Identity Of',
    'Mercury Rising',
    'Alphabetical Code',
    'Trump Administration',
    'Lord Of The Good Tree',
    'The Reincarnation',
    'The Rebirth Is Feared',
    'God Abides In America',
    'Son Of All Forms',
    'Who Is The Antichrist',
    'God Thought',
    'My Birth',
    'Gematria Code Of God',
    'Jewish Gematria',
    'Righteous God',
    'Jesus Cross',
    'And The Lord Shall Be King Over All The Earth',
    'Tree Of Life Anointed One',
    'The Manifestation',
    'Blood Of The Gods',
    'If I Am Jesus Then Why Am I The Man Who',
    'I Am One Of The Ten Names Of Gematria',
    'The Full Armor Of God',
    'Yeheshua',
    'Judge Of Melchizedek',
    'In God Yeshua El Shaddai',
    'Nochebuena',
    'Feliz Navidad',
    'Dreadnought',
    'Jesus Regresa',
    'I Found The Truth',
    'Creator Of Heaven',
    'The Tree Of Life And',
    'The Bible Code Book Of Psalms',
    'Holy Spirit Communication',
    'Jesus Christ Is States',
    'Flesh And Blood Death And Blood',
    'The Peace Of The Lord',
    'Jesus Is God Christ God Yhwh',
    'The Day Of Prayer Jesus Christ',
    'The Appearance Of The Holy Spirit',
    'I Am Only The Best And Light Bringer',
    'I Am Lord Jesus Christ',
    'Satan Back Yourself The Lord',
    'Five Five Five Light',
    'Jesus Setravalo G',
    'The Coming Of The Lord God Almighty',
    'The People Of The Church Of The Holy Trinity',
    'I Am Christos Creator Power And That Shows My Faith',
    'The One Who Is To Come Over Heaven And Earth',
    'Jesus Saw The Final Location Gave Out For All Fucking',
    'The Lamb Stood Upon The Foundation Of The World',
    'Numbers Where My Number',
    'El Cristo Negro Revealed I Am Here In The',
    "It's Now Revealed If You Have Understood The",
    'Subject The Dream Car',
    'My Power Of Sight Insights Into God',
    'Morningstar',
    'Lucifer Was Born On May Five',
    'The Pure Doctrine Of',
    'The Holy Grail Is The Creed Of Yeshua Christ',
    'God Speaks Through Numbers May Five One Forty',
    'Christ Is Already Here And They Are Forbidding His',
    'Yeheshua Birth Fifth Seventy Two',
    'The Mercury Secrets',
    'Mourning Is Mercury',
    'Yhwh Has Forgiven',
    'I Glory In Salvation',
    'God Knows My Identity',
    'The Lord Living God Yhwh Elohim',
    'Gods Chosen One For My Name Is',
    'The Light Bringer Of Lucifer',
    'How Much Is The Pure Doctrine Of',
    'The Holy Death Is The Soul Of Jesus Christ',
    'Christ Of Nazaret Is Ready To',
    'Jesus Christ Of Nazareth',
    'The Manifestation Of Lucifer',
    'Birth Of The Earth Campain',
    'The Holy Bible Is A Secret Script',
    'The Nation Sees The Virgin Lifting',
    'Jesus Son Of The Holy Spirit',
    'I Am Jesus The Savior',
    'I James Campain A Christ',
    'God Within The Body',
    'Scriptures',
    'Jesus Christ Is Reincarnated',
    'The Vatican Antichrist',
    'The Grandson Of Jesus',
    'I Am Born The Messiah Yeshua',
    'Jesus Christ To Save The World',
    'Forever Jesus',
    'Almighty God Of The New Revelation',
    'Heaven Etymology',
    'The Revelation Of Truth',
    'The Abomination Of Humanity',
    'The Final Dragon Royal Blood Line',
    'Christ Is A State Of Consciousness',
    'The Green River Prophecies',
    'Who Is Jesus Christ Know',
    'The Arc Revealed The End Decoded',
    'The King Is The Only Just Sword',
    'Holy Human Holy Spirit',
    'Picture Of Jesus Christ',
    'The Holy Spirit Of The Bible',
    'Everyone Says I Am The Messiah',
    'Gematria Says I Am The Messiah',
    'Jesus Yeshua Prophecies A Birth',
    'I Used Sacred Name Of The Lion Of Judah',
    'Anti Christ Born May Fifth Seventy Two',
    'Lucifer Was Born On May Fifth',
    'Who Is Messiah Jesus Messiah',
    'Holy Ghost Is Lord And Holy Spirit',
    'I Am Worthy Of The Precious Of The Christ',
    'Who Is The Wisest Man In The World',
    'Jesus Would Fulfill The Will Of His Father',
    'The Way Of Joy',
    'Absolute Precision Intelligence Message From God',
    'The Second Coming Of Jesus Is Now',
    'The Kingdom Of God Is Here And They Can Stop I',
    'Holy God Mary Magdalene Yeshua',
    'King David Reborn Saves',
    'Victory Of The Holy Spirit',
    'The Holy Ghost Is Lord And Holy Spirit',
    'Only God Exists I Am Coming',
    'Open Your Eyes My Sons',
    'Holy Spirit The Son Of God The Creator Of The Universe',
    'Seven Seven Seven',
    'I Am The Chosen Son Of Man And The Root Of David',
    'The Lord Speaks Through Love',
    'A Spirit Reincarnated In New Body',
    'Glory Of God Total Fullness Of The Heart',
    'God Benefits To Alex Campain',
    'Reveal Secret Truth',
    'The String I Need You To Untie',
    'The Power Of Three Six And Nine',
    'The Final Mystery Is Reborn',
    'God Revelation To Alex Campain',
    'The Name One And Only I Am Not Saying Anything Yet',
    'God Speaks Through Numbers Jesus Christ To Alex',
    'The Tree Of Knowledge',
    'I Am In The Spirit In The Flesh',
    'Jesus Of Nazareth Living Son Of God',
    'Decode The Go To Herald Of The Second Christ',
    'The New Christ Is Lord',
    'An Encoded Code Encrypted Before The Beginning Of Time',
    'I Am The King Of All I Am All',
    'The Anti Christ Is Alex Campain',
    'Bloodline Of The Heavens',
    'The Anointed Messenger Of God',
    'Incarnation Of Jesus Magdalene',
    'This Is The Birth Date And Death Date',
    'Venus The Goddess Messiah',
    'I Impose Absolute Love In The Name Of Jesus',
    'I Am Waiting For Jesus',
    'Holy Spirit Born A God',
    'May Fifth One Forty Four',
    'Christ Versus The Messiah',
    'Confess Jesus I See God Son Of God',
    'The House Of Holy Spirit',
    'The Authority God',
    'The Anti Christ Is Anti Satan',
    'The Number Of The Antichrist',
    'The Four Horsemen Of The Apocalypse',
    'Lucifer And Satan Last To God And Jesus',
    'The Second Coming Of Jesus Will Be Revealed D',
    'The Ideal Dragon Royal Blood Line',
    'God Tells Alex Campain You Are The',
    'The Spirit Of Jesus',
    'Crown Of Thrones',
    'Birth Of Holy One K God',
    'The Dove And The Phoenix',
    'Jesus I Am The Lord Christ',
    'The Holy Bible Is The Greatest Of All',
    'Jesus Christ Life I Am That I Am',
    'I Am Alpha And Omega',
    'Anti Christ',
    'Second Coming',
    'Im Alex Campain',
    'Devil Lucifer',
    'Nine Nine Nine',
    'Five Five Five',
    'Host Body Yehoshua',
    'The Forces Of Darkness',
    'The Art Of The Covenant',
    'Number Eight',
    'Number Of Man',
    'Doing The Miracle Math',
    'Jesus Blood',
    'Star Of Bethlehem',
    'Mr Alex Enrique Campain',
    'The Reincarnation Of The Anointed',
    'The God Of Heaven',
    'Only Begotten Son',
    'The Son Of Man Revealed',
    'Lamb Of God Is Alex Campain',
    'I Am May Five',
    'Decode Messiah Christ',
    'El Senor Alex Campain',
    'The True Existence Of Lucifer',
    'I Am The Destroyer Of Devils',
    'God Reveals To Alex Campain You Are',
    'The Anointed King Of The Daivdic Line',
    'The Five Of Lord Jesus Christ',
    'Holy Translation Of God Codes',
    'Good Holy Body The Trinity Perfected Mr',
    'Christ Jesus Is The Messiah',
    'Holy God Triple Dna Children Covered',
    'The Spirit Of The Lord Is Upon Me The Messiah',
    'Jesus Returns With A New Name',
    'Campain May Fifth Nineteen Seventy Two',
    'Lord Who Is Your God I Am I Am',
    'Second Coming Jesus Has Arrived',
    'Jesus Christ I Except You',
    'City Of Lucifer In The Kingdom Of Heaven',
    'Letteraeria',
    'Our Lord Jesus Christ Of Letteraeria',
    'The Lord Teaches Quantum Physics I Am',
    'The Greatest Of Any Father God Ever Had',
    'King And Queen Come To The New Kingdom',
    'Lord Jesus Christ Suppressed No Longer',
    'Alex Campain Es Jesucristo Cristo',
    'United States Dollar',
    'Antichrist Calculator',
    'The Holy One',
    'Menschenstreik',
    'Merovingian',
    'Apocotypes',
    'Christian Sing',
    'Vatican City',
    'The Stone Of God',
    'Joshua Tree',
    'Prophecy',
    'Completion',
    'Aquarius',
    'In The Truth',
    'Children Of Joseph',
    'Lord God On A Throne R',
    'God Bless Us All',
    'Holy Father God',
    'The Holy Lands Of God',
    'Holy Angelic Holy Spirit',
    'I Am The Holy Son',
    'Who Is The Destroyer',
    'The Redeemer Savior God I Am I Am',
    'The Red Dragon Lord',
    'Jesus Christ Is God In The Flesh',
    'Donald Trump Ill Be President',
    'Alex Enrique Campain May Five',
    'Son Of Man Savior',
    'The Fast Doctrine Of Lucifer',
    'Jesus Christ Born May Fifth',
    'Campain May Five Nineteen Seventy',
    'The Root And The Offspring Of David',
    'Alex Campain The',
    'Jesus Christ King Of Kings And Lord Of Lords',
    'The Root Of David The Single Morning Star',
    'The Most High Man Is God',
    'The Most High Man Is God He',
    'Width Of God',
    'Horn Of Salvation',
    'Yahweh The Son',
    'The Sword Of The Trumpet',
    'Antichrist',
    'The Mandela Effect',
    'The Sea Of God',
    'The True God Is The Lord Shepherd',
    'Raise Vibe Frequency K G',
    'The Encoded Ends Christ Of Elijah Micah',
    'The Lords Eyes',
    'God Revealed Is Heaven',
    'Yeshua The Christ',
    'Yes He Created Everything',
    'Jesus Is The Messiah Passed',
    'I Am King Of Green And The Lord Of Lords',
    'The Antichrist Secret Society Of Christ',
    'Christus',
    'Antichristos',
    'Alex Campain Messiah',
    'The Living God',
    'The Divine Child',
    'Lucifer Reincarnation Fire',
    'Jesus Christ The',
    'Yehowshua Son Hidden',
    'True Deliverance From God',
    'Sons Of The Unknown God',
    'Jesus The Perfect Coder Of Codes',
    'Child Of Yahweh',
    'A Gift From God',
    'Gods Perfection',
    'The Lords Codes',
    'God Almighty',
    'Everybody',
    'I Am Alex E Campain',
    'Decode Yhwh Vav Shin Ayin',
    'Decode Sword Of The Spirit',
    'The Unknown Creator',
    'Holy Spirit Divine Gene',
    'Interconnected In Number',
    'Lord Jesus Christ Throne',
    'Secret Lord Jesus Christ',
    'Jesus Christ Translate',
    'Jesus The Exemplar Of Resurrection',
    'Blood Of My Blood',
    'Two',
    'The Three Angels Of Truth And The Life',
    'God God God God',
    'King D King Of Lords Melchizedek Al Malik',
    'The White Horse Is Coming To All Peoples Will Answer To',
    'The Birth Date And Return Of Christ Jesus',
    'Jesus Died The Day He Was Murdered',
    'For His',
    'The Meaning Of Number Nine',
    'Center Of The Universe',
    'The French Connection',
    'Jesus Is Christos',
    'Spirit Mahdi God',
    'The Transfiguration',
    'In The Name Of Truth',
    'I Am E Campain Son Of God',
    'Son Of God Is Alex Enrique Campain',
    'The Messiah God In The Flesh',
    'Divine',
    'Alex Campain Son Of God',
    'The Holy Spirit Of Truth',
    'One One Four Four',
    'The Son Of God Revealed',
    'Jesus Was The Light Bringer',
    'Jupiter Venus Alignments',
    'Alexander Campain Is The Son Of God Father',
    'Father Son Holy Spirit Trinity',
    'I Love Love Love Love You',
    'Holy Holy Holy Is The Lord God Almighty',
    'Messianic Messiah Jesus',
    'The Kingdom Of God Is Coming And They Cant Stop It',
    'Jesus Is The Way The Truth And The Life',
    'Decode Mary Magdalene Jesus Christ',
    'I Am The Christ And There That Are Against Me Are My',
    'Alejandro Enrique Campain May Fifth Nineteen Seventy Two',
    'The True Identity Of Jesus Christ Is Revealed By',
    'I Believe Jesus Is The Son Of The Most High God',
    'I Will Fulfill What He Started',
    'Fight Fight Fight Alex Enrique Campain',
    'Rose Of Jesus',
    'The True Holy King',
    'The Signs Of The Rapture',
    'The Risen Lord',
    'Jesus Lucifer Twinflame Name',
    'Gematria Calculator',
    'Jesus The Second Coming Of Jesus Christ',
    'Jesus The Seed',
    'The Star Of Bethlehem',
    'The Final Name',
    'Choose',
    'I Am Alex Campain A',
    'I Am Lucifer Per God',
    'The Mark Of Obedience',
    'The End Of Darkness',
    'Alex Enrique Campain Is The Son Of God Yahweh',
    'Jesus Is The King Of Kings And Lord Of Lords',
    'Yhwh Is Yahweh In Heaven Faces',
    'The Second Coming Of Jesus Will Be Revealed',
    'Six Thanks Alex Campain Is The Christ',
    'Alexander Campain Is The Holy Tree Of God',
    'The Most Important Gematria Code',
    'Hot To The Throne Of King David',
    'The Immanuel Return Of The Lord',
    'The White Horse',
    'Jesus Of Nazareth The King Of The Jews',
    'Karen Is Crytek',
    'The True Anointed Messenger',
    'God Holy Spirit',
    'The True Christ',
    'The Truth Jesus Saves God Yahweh',
    'Alex Enrique Palma Campain Is God Yahweh',
    'The Truth I Am Jesus The True Christ',
    'The King Of The World Of God',
    'United States Of America',
    'The Venus Frequency',
    'I Am The Alpha And The Omega The First And The Last',
    'Name Of Yahweh Almighty We Pray',
    'Virgin Mary Gave Birth To Jesus Christ On May Fifth',
    'Human Rights Everywhere In The Now',
    'Forgive Them Not For They Know Not What They Do',
    'Music',
    'Jesus I Am Sorry For Everything I Love You And',
    'Renewing The Spirit Of Truth In The House Of The Holy',
    'The Wrath Of God',
    'Jesus Cracked The Code',
    'Yhwh The Apocalyptic God',
    'Virgin Mary Gave Birth To Jesus Christ On Five Five',
    'Save Date Of Birth Code Of Birth',
    'Jesus Is God Christ And God Yhwh',
    'The True Messenger Of The Divine Fire',
    'The Apocalyptic God',
    'Spiritual Army',
    'Am The Chosen One',
    'The True Messenger Of The Aquarius age',
    'Holy Birth Of Alex Enrique Campain',
    'I Will Become What God Wants Me To Become',
    'The Divine Trinity Of Heavens Incarnate',
    'Jesus Is The Alpha And The Omega',
    'I Am Who I Am The Messiah Visitor',
    'Test God The Eternal',
    'Jesus Second Coming',
    'Jesus Emmanuel',
    'Holy Birth Of New Enrique Campain',
    'El Dios Adriano Ruiz',
    'Corintios Uno Diez',
    'El Nombre De Dios Es Maria Magdalena',
    'El Salvador Del Mundo',
    'El Verdadero Nombre Del Dios Aláxiseue',
    'Yo Soy El Camino La Verdad Y La Vida',
    'Una Novia De Cristo',
    'Te Tu Novio De Cristo',
    'El Secreto Revelado',
    'Soy La Esposa De Dios',
    'Gris Adriana Ruiz',
    'I Am Hammashiach The King I Am The Alpha And The Omega',
    'What Is The Name',
    'The Holy Birth',
    'Christ The Lord Saves',
    'The Name Jesus The Only Name Under Heaven Gives',
    'Jesus Christ King Of The Jewish People',
    'The Lion Of The Tribe Of Judah Is Alive In The U S A',
    'Jesus Christ King Of Angels And Lord Of Lords',
    'In The Beginning God Created The Heavens And The',
    'Alex Enrique Campain Is The Prophesied Messiah',
    'I Jesus Come To Reclaim',
    'God Comes Man Comes Again',
    'Alex Campain Is The Prophesied Messiah',
    'The Real Sacred Sound Of Gematria Revealed',
    'Jesus Christ Food First Fruit',
    'The True Messiah And The Lord',
    'How Much Is Alex Is Jesus In Gematria What Is The Meaning Of',
    'Fire Five One Nine Seven Two',
    'God Jesus Have Mercy On Me A Sinner',
    'The Alpha And The Omega I Am The',
    'I Am Superintendent Abraham',
    'Trust Messenger Of God',
    'My Son The Son Of Israel',
    'Mighty God Real Prophet',
    'Six Six Six Alex Campain',
    'My Name Is Hibiscus',
    'Meaning Of Sight',
    'True Birthday',
    'The State Of Israel',
    'Prophesied Christ',
    'Head Of God A Christ',
    'Who Understands That Alex Campain Is The Messiah',
    'Reincarnated Lord Jesus',
    'The True Holy Spirit',
    'The Amazing Gene Of The Holy Spirit',
    'The Seven Gifts Of The Holy Spirit',
    "I've Seen God In The Holy",
    'Morning Star The Greatest God',
    'God Knows Alex Campain Is Jesus Christ',
    'Alex Campain May Fifth Is The Son Of God',
    'Descendent Of David Descendent Of David Descendent',
    'Five Five Five Five Five Five Five',
    'The Messiah Is On A Global Deployment M A T C H List',
    'The Almighty Is On A Global Deployment M A T C H List',
    'Access Lord Jesus Christ',
    'God Prediction Book Of The Dead',
    'I Love Jesus I Love You',
    'The Vatican Believes Alex Campain Is The Prophesied Messiah',
    'The Way Is The Path The True And The Life',
    'The King Revealed The King Revealed',
    'What Are We Waiting For Yeshua Has Been Here',
    'How To Win The Powerball Jackpot',
    'Lucifer The Light Is Money The Devil Is Lucifer',
    'The Translation Has Begun All Praises Thank You Adonai',
    'Every Days A New Day To Learn Lessons In Life',
    'The Heavens Of Luciferian Propaganda Will Give Them They',
    'Holy Blood Of Jesus Christ Was Not Spilled In Vain',
    'All People Will Pray To Thee True King Of Kings Lucifer',
    'God Is Very Often Blessed For The Evil That The',
    'The God Of Israel Prophecy Reads Its Kadash',
    'God You Have To Learn About Now',
    'Everything We Have Been Taught Is A Lie By Design',
    'How My Thoughts Produce Your Results',
    'Jesus Christ Revealed By The Order Of Christ',
    'Jesus Christ Of The Undisputed King',
    'They Know Everything You Are Thinking I Need To Be The',
    'The Bible As We Know It Today Is Incomplete And',
    'The Alpha And The Omega The Beginning And The End',
    'The Day The New Day Will Break The Evil That Has Been S H A W N On Earth',
    'The Coming Of Christ And Our Gathering Together Une',
    'Thy Kingdom Come On Earth As It Is In Heaven',
    'Lord Yeshua The Light Of The World',
    'The Vatican Knows Who Alex Campain Is Jesus',
    'My Ancestors Were Beautiful Women Like Moses',
    'The Name That Is The Precious One For All Of This',
    'Jesus Is On Earth Is',
    'The Supreme Commanded King Of All Numbers',
    'Rapture Day Of Jesus',
    'Jesus Christ Ruler Of Heaven And Earth',
    'This',
    'Lucifer Is The Only Spirit Of Mankind',
    'Lord Yeshua Thank You For Saving Me',
    'All Religions Know The Truth',
    'Yeshua Christ Has Returned To Earth',
    'Holy Family Of The Great Tribulation',
    'Jesus Christ Is The Undisputed King',
    'The Second Coming Of Jesus Will Be Known',
    'King Im Here To Reveal The Whole World Will Know',
    'When The Son Of Man Cometh In His Glory And All The Holy Angels With Him',
    'Age Of Aquarius True Human Heart',
    'God Loves Alex Enrique Campain',
    'Decode Jesus Prophecy',
    'The Merovingian Line Of Jesus Christ',
    'The Number Blessed You Are The Lord',
    'Gods Secret Commandments The Only Love',
    'Your Name Is In The Bible New Jerusalem',
    'God Sent Me To Show You The Code Of The',
    'Jesus Christ Perfect Name',
    'The Passion Of The Christ',
    'The Demonization Of The Anointed',
    'I Am God Yhwh The Creator Of The Universe',
    'All The Prophecies Of God Is Jesus Christ',
    'The Prophecies Of Yeshua Christ',
    'The Number Of Synchronicity',
    'The True Name Of The Messiah The Most High God',
    'How Much Is Triple Eight In',
    'I Am Dear God',
    'Who Is The Messiah Jesus',
    'God Forgives Me',
    'The Holy Triple Eight',
    'The Truth Is The Foundation Of The',
    'Alex Campain The Bread Of Life',
    'In The Name Of Justice',
    'The Meaning Of Three Seven',
    'Father Son Holy Spirit',
    'Jesus I Will Spend All Day With You',
    'Decode Yeshua Jesus Yahweh Reborn In',
    'How A Soul Captured Is Incarnated',
    'The True Key Of Salvation',
    'This Is The Key That We Will Need Before Goodbye',
    'This Is The Key To Heaven',
    'The Second Coming Of Christ',
    'Yeshua The Lord Of Lords And King Of Kings',
    'God God God',
    'Monosegui',
    'Jesus God Sex',
    'Gods Achieving',
    'Mary Magdalene',
    'Additional',
    'Triple Eight',
    'How Much Is Who Is Jesus In',
    'How Much Is Save The World Is',
    'Lucifer Is Alex Enrique Palma Campain',
    'The Birth Date And Return Of Jesus Christ',
    'King Kings Lord Of Lords Melchizedek Al Malik',
    'Alex Enrique Palma Campain May Five One Nine Seven',
    'The Lord Jesus Christ Will Be Revealed Through',
    'All Things Are Possible With God',
    'Alex Enrique Is The Son Of God',
    'Burning A Down God',
    'Lord Alex Enrique Campain Is The Son Of God',
    'I Am God Creator Of The Universe',
    'Salvation belongs to our God who sits on the throne and to the Lamb',
    'Alex Enrique Campain is Jesus',
    'Alex Enrique Campain is God YHWH',
    'Jesus Christ On The Cross',
    'Yeshua I Want To Learn From You',
    'Jesus Was Resurrected On May Fifth',
    'Waking Up Jesus',
    'Decode What My Name Reborn From Heaven Is',
    'How Much Is Waking Up Jesus In',
    'I Alex And See',
    'The Lost Messenger Of The',
    'They Are Eternal Life Here',
    'Reincarnation Of Christ',
    'I Am The True Identity Of Christ I Am',
    'God Is Everything',
    'I Am Wealthy',
    'The Virgin Mary',
    'Lucifer The Most Beautiful Angel',
    'The Passion Of Christ Get Lord And Savior',
    'El Coder Cristo',
    'The Prophesied Messiah',
    'Jesus The Son Of Man Returns With A New Name Alex Campain',
    'Jesus Christ Our Lord And Savior Is A Heaven And His',
    'The Son Of Man Alex E Campain Returns With A New Name',
    'I Am Alpha And Omega The End And The Last The Lord',
    'He Is Jesus Of Nazareth The King Of Kings And Lord Of Lords',
    'Jesus Christ Died A Human And His Name Is',
    'The Truth Is Revealed And The Lord I Am',
    'How Much Is Jesus Is Who Is In Gematria What Is The Meaning Of',
    'Crucified Christ Is The Son Of',
    'Son Of Man The Alpha Omega King Of Kings',
    'The Holy Unknown Name Of God',
    'Gods Only Begotten Son',
    'Alex Campain You Are The Only Begotten Son',
    'The Wayfaring Frequency Of Love',
    'Reincarnation Of The True Jesus Christ God',
    'Jesus Of Nazareth Reincarnation See',
    'Reveal The Power Of The Lion Of Judah',
    'Lucifer Is The Most Beautiful Angel',
    'Nightmare Jesus',
    'The Son Of God That',
    'True Revelation From God',
    'My Name Is Yahweh',
    'Jesus Christ The Truth And Light',
    'Redemption Of Jesus Christ The Lord',
    'My Holy Holy Of Yahweh',
    'The Number Of Manifestation',
    'The Holy Holy Of Yahweh',
    'The Lord The Lord I Am',
    'How Much Is Rose Of Jesus In',
    'The Crowned Christ',
    'Dios Sobre Alex Campain',
    'God Of The Aquarian Age',
    'Jesus The Savior',
    'How Much Is The Gospel Of Mary In',
    'Jesus Gata Del Cielo',
    'Hallelujah Jesus',
    'You Are Gods Only Messiah',
    'Nazarean',
    'Reigns On The Throne',
    'Satan And Antichrist',
    'Alex Enrique Campain The Lord Messiah',
    'Alex Campain Is The Son Of God The Savior',
    'The Son Of God Alex Enrique Campain',
    'The Holy Spirit On The Cross Of Christ',
    'I Am Alpha And Omega The First And The Last Reborn',
    'Alex Campain You Are Only Begotten Son',
    'For He Is The Messenger Of The Lord Of Hosts',
    'Armored Messiah Of Lucifer',
    'Anointed Messenger Of Lucifer',
    'Divine Gmatria Jesus Nazaret K',
    'I Am Here To Do Your Will Is What I Shall Be D',
    'Everything Just Works Out For Me',
    'Decode What My Name Before I Was Born Here',
    'Yahweh Confirms Alex Enrique Campain Is Jesus Christ',
    'The Truth Will Set You Free And Bring You Back To Me',
    'The Most Important Relationship Is With Jesus',
    'Jesus Christ The Way The Truth And Light',
    'I Wish That I Could Save The World',
    'Yahweh Confirms Alex Campain Is Jesus Christ',
    'Anointed Messenger Of God',
    'I Am One With The Reincarnation Of',
    'I Will With You In Spirit Until You Are Ready To He',
    'You Are The Son Of God Jesus Christ',
    'The Alpha And Omega The Final Code To Break Christs',
    'Jesus Family Tree',
    'My Body Of Christ',
    'The Old Testament',
    'Throne Of The Lord',
    'The Crucified God',
    'Shed Blood Of Christ',
    'As Prophesied',
    'Just People From The Past',
    'This Is The Way',
    'The Glorified Body',
    'The End Of Lord Jesus Christ',
    'God In This Circle',
    'Glory',
    'Father Of All',
    'Amen',
    'Sun Of God',
    'Moon',
    'Lights',
    'Earth',
    'Universe',
    'The River Runs Back',
    'I Am Here If You Want To Talk To Me',
    'Hear Every Thought',
    'Elvis Presley',
    'I Am Jesus Of Nazareth Living Son Of God',
    'Message From God To Alex Campain',
    'Are You Ready To Be Your Activities',
    'The Savior Of Man',
    'He Who Shall Stir Up The Hook',
    'I Am The Lord Reborn From Ash',
    'This Is The Fire Code',
    'Christ The Lord',
    'Miracle Of Being Christ',
    'Thou Art The Greatest Of The Living God',
    'The Jupiter Loves Humanity',
    'The Future Of Christ As The Lion',
    'The Picture Of Christ As The Lion',
    'Message From Yahweh To Alex Enrique Campain',
    'Everything Is Going To Be Alright',
    'I Know Everything About You',
    'You Are Safe',
    'Give Freedom',
    'How Much Is Phaeton In',
    'Jehovah Code',
    'The True Identity Of Alex Campain',
    'You Are His Only Begotten Son',
    'I Am Ready To Fulfill My Destiny',
    'Return Of Our Lord And Savior',
    'The Incarnation Of Jesus Christ',
    'Jesus Christ Is Alex Enrique Campain',
    'With God Salvation',
    'Jesus Christ Is Alexander E Campain',
    'The Revelation Of Jesus Christ',
    'Messiammessiahjesusmessiahholyjesus',
    'Lord Messiah Son Of Man',
    'The Alpha And The Omega The Last',
    'Know The Truth Alex Campain You Are Yeshua Christ',
    'He Is The Messiah Jesus Christ',
    'Holy Jesus Christ',
    'Yeshua Christ Model Of The Universe',
    'Alejandro Enrique Palma Campain Is The Rose Of Sharon',
    'Love Is Everything',
    'All Are Everywhere',
    'Jesus Christ The Lion Of God The Lion Of Jesus Christ',
    'I Am Prophesied Jesus',
    'Jesus Reborn In Body',
    'Jesus Is Here In Body',
    'The Lord Is Worthy To Open The Book',
    'Decode Jesus Christ Returns As The Lion',
    'The Anointed King Of The Davidic Line',
    'The Lion Of Judah Jesus Messiah',
    'Jesus The Messenger',
    'Alex Enrique Campain You Are The Messiah Yeshua',
    'Who He Is The Lion Of The Tribe Of Judah',
    'The King Of Kings And Lord Of Lords',
    'Alejandro Enrique Campain Is The Lord Jesus Christ',
    'Who Is In The Lion Of The Tribe Of Judah',
    'Yeshua Messiah',
    'Alexander Campain Is The Rose Of Sharon',
    'The Song Of Salvation',
    'Alexander Campain The Rose Of Sharon',
    'The True Reincarnation',
    'The Most Powerful Triple Digit Number',
    'The Holy Spirit Lives Within This Man',
    'Messiah Alejandro E Campain You Are The Son Of God',
    'The Lord Works In Mysterious Ways',
    'Decode I Am The Christ Reborn And The Holy Spirit Of',
    'My Name Is Archangel Michael Lord',
    'Messiah Alexander Palma Campain You Are The Son Of God',
    'Lord Messiah Alex Enrique Campain You Are The Son Of God',
    'The Destiny Of The Universe',
    'The King Jesus Messiah',
    'The Bible Reveals Half To An Open Mind The Lord',
    'The True Messiah Of The',
    'Decode The Birth Of',
    'I Am The Son Of Yahweh',
    'Decode Jesus Christ Divine Gene',
    'This Is The Way The Truth And The Life',
    'The Word Is The Truth In The Word',
    'Jesus Was My Holy Three Pieces Of Peace',
    'Alex Enrique Campain You Are The Son Of God',
    'Megyn Kellys Wedding Ring Diamond',
    'Vatican Hides The Prophecy Of The Bride Of Christ',
    'The Lord God Of Heavens The God Of The Earth',
    'The Truth Always Comes Out',
    'The Lord God Almighty The King Of Kings And Lord Of Lords',
    'How Much Is Alexander In Gematria What Is The Meaning Of',
    'The Bible',
    'Messiah Of The Age Of Aquarius',
    'One Eighty Seven',
    'The Holy Spirit Is',
    'Hebrew Bible',
    'Three Seven',
    'The Davidic Bloodline',
    'The Vatican Address',
    'The True Identity Of Alex E Campain',
    'The Past That You Are All Patriots And Have No',
    'You Are The Messiah Jesus Christ',
    'You Are The Lord Jesus Christ',
    'The Lord Jesus Christ Is Already Here On Earth',
    'The Lord God Of The Great Tribulation',
    'Messiah Is Already Here On Earth',
    'Messiah Alejandro Enrique Campain',
    'The True Process Of The Devil',
    'In The King Of New Jerusalem',
    'Three Hundred Forty Nine',
    'Christ Is Here From The Dead',
    'Acknowledgment',
    'Dos',
    'Jesus Was A Homestead',
    'The Incarnation Of Yahweh',
    'Second Coming Of Jesus Died',
    'Alex Campain Is The Son Of Christ',
    'Blood Of Lord',
    'The Universe',
    'Christ Is King',
    'Son Of Heaven',
    'The Biblical Jesus',
    'One Thousand Years',
    'Eleven Sixty Four',
    'Twins Of God Control The Fate Of The Earth',
    'Morning Star World Kingdom Of God For Faith',
    'Down Four Eight Three Six',
    'A Message From God To Alex E Campain Your Are The',
    'The End Of The Age Of War And The Beginning Of Age Of Peace',
    'Holy Spirit Virtues',
    'The Keys To The Universe',
    'Spirit Man Rules By Love Of The Universe',
    'Destroyer Of Right Hand Man Of The Lord',
    'The Holy Way',
    'Heaven Heaven Heaven Heaven Heaven',
    'Yeshua The Righteous Jesus Christ',
    'A Message From God To Alex Campain Your Are The',
    'The Prophecy Of Synchronicity',
    'Thank You God For Everything',
    'Those Who Oppose The Son Of God Will Be Judge',
    'The Last God That Came And Take The Life',
    'The Day The Lion Of Judah Gave Codes Revealed',
    'Those Who Oppose Alex Campain They Will Be Judge',
    'The Truth About Alex E Campain',
    'The Chosen One Satan Lucifer',
    'Almighty God Of The Great Tribulation',
    'Decode Jesus Reincarnate',
    'True Prophecy God',
    'The Proof Is In The Pudding',
    'The Aquarian Messiah Is Alex Campain',
    'The Creator Of Life On All Dimensions',
    'Alex Enrique Campain Is The Reincarnation Of Jesus',
    'I Feel That The World Is Ready To Receive The Holy',
    'Christ Is A Man Of The Current Coming Age And Is',
    'Jesus Christ The Will Of God Jesus Christ The Love Of God',
    'Social Media Suppression Alex Campain Who Is Jesus',
    'Jesus Christ Reborn On May Fifth Seventy Two',
    'Decode God So Loved The World That He Gave Only',
    'The Most Important Gematria Is In History Of Human',
    'The Final Code To Break Christs Second Coming All',
    'The Vatican Believes They Know The',
    'Jesus Of Nazareth Gives The Sun To The World',
    'In The Beginning God Created The Heavens And The Earth',
    'Yhwh Yeshua Messiah',
    'Lead Yeshua The Light Of The World',
    'The Father The Son The Holy Spirit And Fox',
    'Alex Campain Is The Son Of Yahweh',
    'I Am The Way The Truth And The Life Light',
    'Vatican Suppression Alex Campain They Know He Is',
    'I Am Guarded By Millions Of Angels Working Will Stop',
    'I Am The Lord God Almighty The God Of Gods The One',
    'May Everyone Who Has Ever Met Me Believe The',
    'The Seed Has Descended That People Will Acknowledge',
    'God Said That The Light Was Good And He Separated',
    'You Know What They Are Doing Is Wrong If Yes Only',
    'Thank You Jesus I Am The Truth The Way And The Light',
    'Alex Enrique Campain Is The Son Of Yahweh',
    'I Am The Alpha And The Omega I Am The First And The Last',
    'Vatican Knows Alex Campain',
    'How Much Is Anti Christ In',
    'Christ Has Returned With A New Name',
    'Messiammessiahjesusmessiahjesus',
    'I Am Learning How To Manipulate The Elements To Which',
    'The Spirituality Code Of Our Lord Jesus Christ',
    'Run The Holy Math Fullness Of Revelation Prophecy',
    'Yahweh Yhwh Yahweh Yahweh',
    'Jesus Christ Has Returned With A New Name King',
    'The Book Of Revelation Chapter Five Verse Seventh',
    'God Is Now Here In The Flesh The Earth',
    'One One One One God One God One',
    'Jesus Christ Is The Answer To Everything',
    'True Identity Of Alex E Campain',
    'The Story Of My Life Complete',
    'Holy Grail Reincarnation Of God',
    'The Triple Eight Gods Is Normal',
    'Holy Holy Holy Spirit',
    'Jesus Christ Is A Heaven And His Name Is',
    'Manifest To The World The Messiah Made By God',
    'Remember Your Gmatria The Mission',
    'I Am Responsible For Bringing Heavens On Earth',
    'The Birth Of Christ And Social Security Number',
    'The Wicked Do Not Get To Survive Opposition',
    'Kabbalah Unlocking The Sealed Book Of Revelation Five And',
    'Jesus Is Alex A Male The Only Son Of God Created By',
    'Six Six Three Three Four Seven Five',
    'Right Frequency And Time Indeed',
    'The Messiah Is In The King Of Kings World',
    'Decode English Gematria Calculator',
    'Decode Jesus Gematria Calculator',
    'The Only Spirit Is In The Flesh',
    'Jesus Creator Of The Universe',
    'The Holy Spirit The God Of All Sin',
    'Lord The Original Name Above All Names',
    'Your Identities Will Be Revealed',
    'The Return Of Our Lord And Savior',
    'How Much Is Yahweh Incarnated In Gmatria',
    'Jesus Christ Gods Son Savior',
    'The Truth Is Right In Front OF You',
    'The Father Of The Expectation',
    'We Understand Jesus Messiah',
    'The Great Academy Of Heavenly Man Has Come',
    'The Vatican Knows Alex Campain Is God',
    'Christ Is A Man Of The Current Coming Age And Is Alex Enrique CampainImage Of Gematria',
    'Son Of Man Is',
    'Return On Earth',
    'Jesus Christ Reborn As The Lion',
    'Alex Campain And His Mother Virgin Mary',
    'Gematria Prophecy',
    'The Commandments',
    'Seed Of Life',
    'Jewish Gospel',
    'The Tribe Of The Living God',
    'The True Living God',
    'Alex Campain And His Mother Mary',
    'I Am Yahweh Alex E Campain Is Jesus Christ',
    'I Am Yahweh Alex Enrique Campain Is My Only Begotten',
    'I Am The Christ The Only Son The Comforter',
    'The Living Word Of Yahweh',
    'The Messiah',
    'Holy Grail',
    'How Much Is Holy Grail In Gematria',
    'The Birth Of Christ God',
    'The Eternal Coming',
    'Fifty Three Thousand Jesus',
    'Jesus Immaculate Conception',
    'The Spirit Of The Lord In His Captain',
    'The Son Of God The Lord',
    'I Am The Alpha And The Omega The Living And Dead',
    'Jesus Christ The Only Way',
    'Anti Christ Alex Campain May Five',
    'The Modern Almighty God',
    'The Hidden One Becomes Decoded',
    'The Lord The Lord Prophesied',
    'Jesus Yhwh',
    'The Meaning Of Number Five The Path Of Salvation',
    'The Hand Of God',
    'Day Of The End',
    'Word Of God',
    'Father Son And Holy Spirit',
    'Holy Holy Of God',
    'Only Jesus Son Of God',
    'I Am The Crucified Jesus',
    'Alex Campain The Lord Messiah',
    'How Much Is Aec May Fifth In Gematria What Is The Meaning Of',
    'The Bible Will Be An Archangel',
    'The Holy Spirit Is In The Flesh',
    'Am The Crucified Jesus',
    'I Am Yahweh Alex E Campain In Jesus Christ',
    'The Tribe Who Will Become An Archangel',
    'The Living Word',
    'Only Jesus Son OfGod',
    'Jesus Christ The Abomination Of Desolation',
    'Aware Of A Special Message For You That Comes From',
    'The Truth Will Set You Free And Brings You Back To',
    'My Father Is Creator Of The Elohim',
    'The Current Son Of Jesus Christ',
    'The Year Jesus Christ Comes To The World',
    'The Year God Comes To The World',
    'High Frequency Code For Peaceful Progress',
    'The Encrypted Decryption Of Humanity',
    'In Yeshua Reborn Body',
    'Nag Hammadi Holy Family Of The Triple Eight',
    'Savior Son Of Christ',
    'God Chose You No Coincidence Take Off The Masks',
    'The Birth Of Jesus Christ Our Savior',
    'Lord Yeshua Our Savior',
    'V R Reborn Holy',
    'Alex Enrique Campain You Are The',
    'The Kingdom Come Thy Will Be Done',
    'Have No Doubt Alex Enrique Campain Is Jesus',
    'Everything Moves By Numerology',
    'When Did Jesus Christ Reincarnate',
    'Jesus Christ Was Born On This Day',
    'All Glory Be To The Jehovah And Jesus',
    'The Hidden Secrets',
    'Jesus Is Lord',
    'Christ Cross',
    'Jesus Christ Is Man',
    'The King Christ',
    'Fifth Dimension',
    'The Christ Key',
    'The Christ Is Reincarnated In',
    'Alpha Omega In May',
    'I Am Lord Yeshua',
    'Jesus Father',
    'God Is Lord Yeshua',
    'The Most Powerful Angel',
    'The Day When Jesus Christ Reincarnate',
    'The Kingdom Come Thy Will Be Done On Earth As It Is In Heaven',
    'Messiah Jesus Israel',
    'The Way Is The',
    'The Son Of Man And The Living God',
    'Who Jesus Christ Man Reincarnated Into',
    'Seven Six Hundred Sixty Six',
    'Gematria Prediction System',
    'The Human Body Of God Is',
    'The Ark Of The Covenant Is The Holy Hagiah',
    'The Father The Son The Holy Ghost And You',
    'Mr Son Who Died Once On The',
    'My Son The Branch Of Israel',
    'Mighty God Real Prophecy',
    'All Forms Of Enlightenment Are Here And Now',
    'The Fountain Of Living Waters',
    'The New Age Of Enlightenment',
    'Six Six Six Also Reincarnate',
    'The Lord Christ',
    'Lord Jesus',
    'Yhwh Yhwh Yhwh',
    'Birth May Fifth Nineteen Seventy Two',
    'The Alphabet',
    'El Salvador',
    'My Alexandro E P Campain',
    'Reveal Secret Rapture',
    'The Great Sign And Wonders',
    'My Mission On The Earth',
    'The Man God Delivered To Judge The World',
    'The God Of Numbers',
    'Who Yhwh Is',
    'My Mission On The Lord',
    'The Messiah God Delivered To Judge The World',
    'Intervention',
    'Hold Order Coming',
    'The Flower Of Life',
    'Alejandro Campain And The Black Madonna',
    'Thank You My Universe',
    'Alex Campain The Black Madonna',
    'His Aligning Spirit With God',
    'God Jesus Is Defending',
    'Decoded To Rule The World',
    'The Periodic Table Of Elements',
    'Decoder Of Lives',
    'Decode The Ola Is Pearl Of The Second Christ',
    'The Lord Of The World Revealed',
    'Secret Ends Of The Prophesies',
    'Explosive Gmatria',
    'Yeshua Christ Our Lord And Savior Was Born On This Day',
    'Born On A Friday May Fifth Nineteen Seventy Two At One Forty Four',
    'Jesus Christ Of Nazareth Birthday',
    'Forty Two',
    'Jesus Christo',
    'One Five Two',
    'Oliver Alex Campain',
    'Alexander Enrique Campain And The Black Madonna',
    'Kabbalah Tree Of Life Fibonacci Sequence',
    'Are You Ready To Meet Jesus',
    'God Is My Number',
    'The Purpose Of Eternity',
    'The Most Important To The Queen One',
    'One Four Four Thousand',
    'The Church Of God The Lion Of Judah',
    'Will The Lord God Jesus Christ Come',
    'I Love You Jesus',
    'The Last Trumpet',
    'The Ordinal Numbers',
    'Q Quantum Math Code Gematria Records Code Q',
    'The Light Of Christ Is Born Again Through Love',
    'Holy Mother And Godhead Of The Universe',
    'Do You Understand The Prophecy Of God',
    'I Have Come To Show What I Bought With My Blood',
    'Jesus Saves My Decisions',
    'Angel Reincarnation Has Returned',
    'God Is Not A Religion',
    'I Am Partnering A Miracle Into Today',
    'Secrets Of Who Is Born In The Flesh',
    'Reveal Decode For Consciousness',
    'Gods Points To Encoded In Humans Dna Strands',
    'You Are The True Prophet',
    'The Mother Of The New World',
    'Lord Jesus Christ Is The Force',
    'You Will With Jesus',
    'Jupiter Has Ascended',
    'Decode Jesus Hebrew',
    'I Am The True Prophet',
    'Man Is In The Military',
    'Bible Code Gematria Jesus Christ',
    'Gifted Choosing Of Almighty God',
    'Victim Of God Of This Insane Bible',
    'Found Proof Of Christ The Next Messiah',
    'The Unknown Name Of God',
    'My Birth Name Is Legal Name My Right Name',
    'Holy Spirit Served As The Lion',
    'The Humiliation Of Luciferic Devils Name',
    'Thou Shall Not Worship False Gods',
    'The Holy Spirit Is In Gods Hands',
    'Decode Trinity Of Almighty God',
    'How Much Is Jesus Ascension In Gematria What Is The Meaning Of',
    'Christ Adopted All Seven Children',
    'The Creation Of New Jerusalem',
    'I Am The Son Of God The Prophet',
    'The The Ten Commandments',
    'Supreme Heavens Of God',
    'Jesus Christ Our Lord And Savior Born On This Day',
    'Jesus Christ Of Nazareth Lord And Savior Born On This Day may Five Nineteen Seventy Two',
    'Yeshua Messiah El Shaddai',
    'Absolutely Perfect',
    'Be A Shroud Of Turin',
    'The Periodic Table Of The Elements',
    'The Eternal Holy Trinity Of Heaven',
    'The Numbers Of The Letters A Through Z',
    'You Were Trained From Birth To Do This',
    'I Am The Supreme God For Jesus Of Nazareth',
    "Jupiter's Wisdom",
    'Viva Christa Rey',
    'Prophecy Fullness Of The Word Of God',
    'Mr The Holy Spirit The Father Of Christ',
    'Name Of The Person That Breaks The Masks',
    'God Jesus Is Son Of God God',
    'The Two Other Trees',
    'Alex Enrique Palma Campain May 5th',
    'Happy Birthday Jesus Yes I Am Messiah We Love You',
    'How Much Is Yeshua Christ In Gematria What Is The Meaning Of',
    'The Messiah Incarnated In Jesus Christ',
    'Yeshua Incarnated Into Alex Enrique Palma',
    'I Am The Holy Spirit And Have The Power To Resurrect',
    'The Most Made Flesh Is The True',
    'Thank You Jesus Christ For Caring About Me',
    'Yes I Know I Am Highly Guarded On The King After All',
    'The Blood Of Jonas Christ That Was Shed For Us At Calvary',
    'They Are Christ And They Are Alive Among Us',
    'I Am The Appointed Savior Through The Genes',
    'The Number Of The Letters A Through Z',
    'Month Of The Lamb',
    'The Son Of Christ',
    'The Great Awakening Of Humanity Has Revealed',
    'Blood Of Jesus On The Ark Of The Covenant',
    'One Two Three Four Five Six Seven Eight',
    'Decode The Sacred Return Of Jesus Christ',
    'The Blood Of Jesus On The Ark Of The Covenant',
    'The Mathematical Proof Of Reincarnation',
    'Two Nations Redeem The Messiah Will Come',
    'How Much Is Yahweh In Gmatria What Is The Meaning Of',
    'Reincarnation Yeshua Yahweh In',
    'My Father Created The Seed Of Life And I Am The Word',
    'Get Your Pilot',
    'The End Of All Propaganda Of A New Age',
    'Jehovah',
    'G T The One God Jesus Christ',
    'The Lord Shall Fight For You',
    'Holy Favorite Side Of The Strike',
    'Thank You God For Saving Me',
    'All Is Revealed',
    'Chosen By The Holy Spirit',
    'The End Of The World And Heaven Declares',
    'I Am King In Heaven',
    'Prophesied Jesus Is My King',
    'Lucifer Morningstar The Luciferian Son',
    'The World We Are Know Is Coming To An End',
    'The Book Of Jesus Christ Is The Final',
    'The Lord Of The Tower Of Bubble',
    'God Decodes The World Campain Antichrist Now',
    'Kingdoms Of God',
    'The Holy Bible',
    'Alex E Campain Is You Are Jesus Christ',
    'Jesus Of Nazareth King Of The Jews',
    'Storm Of Truth And Justice',
    'My God Will May May',
    'The Trinity Of Heaven',
    'Holy Windows Of All Creation',
    'You Were Given Gods Birth To This',
    'The Final Code To Break Christs Second Coming',
    'The Kingdom Come The Will Be Done',
    'The Last Prophecy',
    'The Secret Cord Of The',
    'Jesus Christ Is More',
    'Jesus God Immanuel True God Of The',
    'El Cristo Divine',
    'Alex Campain The Messiah',
    'Six One Two Three One',
    'Thy Kingdom Come Thy Will Be Done On Earth As It Is In Jesus Name Amen',
    'One Fifty Two',
    'Christmas Tree',
    'God Secret Plan',
    "God's Prediction Book",
    'Almighty God Is Person',
    'Shatans About Melchizedek',
    'The Prophecy Of Jesus Of Nazareth',
    'Spirit Of Christ',
    'Connecting Lion Of The Tribe Of Judah',
    'You Are Jupiter',
    'The Five Five Five Abundance Alejandro',
    'Give The Evidence To Me',
    'The Second Coming Will Be Hated',
    'Jesus Reincarnated Into Alejandro',
    'Alex Campain You Are The',
    'How Much Is Who Is Alex Enrique In',
    'Christ Reborn',
    'Trust The Plan',
    'God Of The Covenant',
    'Genesis One Seven Seven Name',
    'The Life Of Jesus Christ A Life Of Jesus',
    'Who Is Christ The Savior',
    'The Most High God In The Flesh',
    'Jesus In The Son Of God',
    'The Antichrist The Anointed One',
    'The Lucifer Prophecy',
    'All Glory To God',
    'Yod The Father',
    'The Numbers Of The Bible',
    'I Am That I Am',
    'Name Of God',
    'The Coming Soon',
    'Jesus Christ In The Son Of God',
    'How Much Is Jesus Christ In Gematria What Is The Meaning Of',
    'Lord Alex E Campain',
    'Who Is Yeshua Hamashiach',
    'Who Is In Yeshua Christ Theory From Seller',
    'The Biblical Truth Lucifer',
    'Jesus Messiah Of Nazareth',
    'The King Is Back World Reincarnate',
    'Yeshua Yhwh Yahweh',
    'I Am In The Flesh I Am The Spirit',
    'My Precious Love God Gave',
    'Who Is The Savior',
    'I Am The Way The Truth And The Life Messiah',
    'Six Hundred Sixty Six Code',
    'Those Who Wake Up My People',
    'Resurrection Of Word',
    'Electrical Love Of The Heavens',
    'I Will Speak My Life',
    'The Encrypted Code Knows Love In Code',
    'Anti Christ Bring My Home',
    'I Am The Love That Want To Kill',
    'Christ Revealed And Unsealed',
    'The God Man A Messianic Seal',
    'The Real Messiah Of Jesus Christ',
    'He Is The Lion Of The Tribe Of Judah',
    'The Two Hundred Years Of Christ',
    'The Flat Messiah Of Jesus Christ Child',
    'Alex Campain And Shekinah',
    'The Two Way Swords Of Christ',
    'I Jesus Human Parts',
    'The Holy God And One',
    'How Much Is Lord Alex E Campain In Gematria What Is The Meaning Of',
    'Messiah Is Yeshua',
    'Sea Of The Lord',
    'V V Messiah',
    'Jesus Christ Our Lord And Savior',
    'Jesus Christ Is The Lord And Savior',
    'Jesus Is Christ Our Lord And Savior',
    'Jesus Christ Is Our Lord And Savior',
    'Jesus Christ Is Lord And Savior',
    'Out Of Caleb',
    'How Much Is Out Of Caleb In Gmatria',
    'I Am Yhwh',
    'How Much Is World Peace In Gematria What Is The Meaning Of',
    'Prophecy Of Military',
    'D E P R A H',
    'The Tree Of Life',
    'The Final Creature Constant',
    'Be A Reflection Messiah',
    'The Righteous Proof',
    'Christ Resurrection',
    'A Paragraph And Magnificent King Of Kings',
    'An Honorable And Magnificent King Of Kings',
    'Services',
    'Quantum Mechanics',
    'Alex Campain And The Black Madonna',
    'Bright Morning Star',
    'The Picture Of Christ',
    'The President Of The UnitedS tates',
    'Lion Of Judah Descendant',
    'James Christ Four Four Four Four',
    'You Were Jesus',
    'The Holy Magdalen Is The Blood Of',
    'Sheol Of Turin',
    'Jesus God Jehovah',
    'Yhwh Hamashiach',
    'Love Frequency',
    'Kingman',
    'The Name Alpha And Omega Birth',
    'Forgiveness',
    'Ring Of The World',
    'Alejandro Enrique Palma Campain Is The Son Of God',
    'The Holy Spirit Symbol Apocalypse',
    'The Proof Of The Immaculate Conception',
    'Ability To Change The World Is Divine Gene',
    'Where Is He Now',
    'Alex Campain Is The Son Of God Yahweh',
    'The Holy Key',
    'The Chosen One May Explain',
    'Chosen Of England',
    'I Am Alpha And Omega The Beginning And The End',
    'The True Messiah Of Israel',
    'Jesus Christ Global War Campain',
    'The Gematria Awakening Of Humanity Now',
    'He Is The Unbreakable Proof Of Corruption Ascension',
    'Decode This Is The Dawning Of The Age Of Aquarius',
    'The Holy Magdalen Is The Blood Of Christ',
    'Jesus Prophet',
    'The Christ And He Is Alive Among Us',
    'The Biblical Antichrist X',
    'The Chosen One May Fifth',
    'Eighth',
    'Kingdom',
    'Zero Zero Zero One Two Vatican City',
    'You Are The Son Of Christ',
    'I Am One With The Devil That Has Been Reincarnated',
    'May Fifth Nineteen Seventy Two One Four',
    'Who Is Alex Enrique Campain The Messiah',
    'Three Hundred Army',
    'Jesus The Redeemer',
    'The Blood Of The Lamb',
    'I Am The General Coming Of Christ The Savior',
    'The Davidic Shield Of David',
    'The Fibonic Field Is The Unified Field Of Consciousness',
    'Track In Terms Of Energy Frequency And Vibration',
    'Alejandro Enrique Palma Campain May 5 1972',
    'Yod Hei Vav Hei',
    'The Return Of Christ The Lion',
    'The Aquarian Age',
    'He Is Adonai',
    'You Really Are The Second Coming Of Christ',
    'The Apocalyptic Second Coming Of Christ',
    'In The Gmatria Code Of The Holy Spirit',
    'The Constant Sign Is To Believe The Truth Of God',
    'Jesus Christ Teaches Quantum Physics Fluids',
    'God Given Name Alex Campain',
    'How Much Is Yud Kei Wav Hei In',
    'The Last Twenty Six Letters Of The Alphabet',
    'The Best Secret Of Gmatria Revealed',
    'Jehovah Yahweh The Marriage',
    'The Bible Is In Truth',
    'Kindness Is Godliness',
    'Twenty Square',
    'The Tetragammaton',
    'Divine Code Of The Christ',
    'Messiah Of Christ',
    'Alex Enrique Palma Campain Is The Messiah',
    'Bloodline Of Jesus',
    'The Blood Behind The Cross',
    'Restoration The Son Of God',
    'Last Number Four',
    'There Are No Coincidence True Prophet Of God',
    'My Kingdom Will Never Be Destroyed',
    'Sciences Does Not Understand The Universe',
    'The Big Bang That All Humanity Is Waiting For Good',
    'The True Name Of The Messiah The',
    'Thank You God Grand Master Creator For This Day',
    'Decode Jesus Christ King Of Kings And Lord Of Lords',
    'Jesus Arose On The Third Day From The Dead',
    'The Reason For This Life Being',
    'The Love Of Jesus Christ',
    'King Of The World',
    'Nothing Can Stop What Is Coming',
    'Alex Enrique Campain The Son Of God',
    'Vatican Address',
    'Lord I Am Speaking Some Of God',
    'How Much Is Lord Alex E Campain In',
    'God Yahweh Identified',
    'Señor Alex Y Campain',
    'La Santa Biblia',
    'The Truth Is In Front Of You',
    'My Name Is Alex Campain I Am The Alphabet',
    'I Am Yahweh My Son Alex Is In The Alphabet',
    'Jesus Yahweh My Son Alex Is In The Alphabet',
    'Is Heavenly Worth My Spirits',
    'Install The Plan To Save The World',
    'I Am The Lion That Must Be Told',
    'The Senior Jesus Christ The Lord',
    'I Am The Royal Blood The Real',
    'Jesus Is The True Messiah',
    'I Am The Son Asking To Understand',
    'Only God Will Do Know Who You Are',
    'Years Gonna See The Coming Of The Lord',
    'Alex Campain Is In The Alphabet',
    'Seconds Is In The Name Of Jesus Christ',
    'I Believe In Jesus',
    'The Truth Will Shock The World',
    'You Are The Second Coming Of Christ',
    'I Am Yahweh My Son Alex Am Is In The Alphabet',
    'The Doomsday Clock',
    'Protection That Prevents Evil And',
    'Just Sing Love',
    'Thank You Father',
    'Secret Of Three Six Nine',
    'The Alpha Omega Gene',
    'Mrs Match Is The Book Of Enoch The Book Of C',
    'Holy Holy Holy Blessed Is The Name Of The Lord',
    'Everyone Is Saved',
    'Oh Much Is The Purpose Of A Human Sacrifice',
    'Pontius Pilate Crucified Alexander E Campain',
    'The True God Is In The Flesh',
    'The Mother Spirit Of Rebirth And Renewal',
    'I Am Getting Closer To All The Hidden Truth',
    'Beyond The World',
    'I Am The Holy Spirit Have The Power To Resurrect',
    'Bringing All Man To One Collective Understanding',
    'The World Is Encoded Jesus Name',
    'The Man Of God Is Jesus Christ',
    'Aquarian Sagittarius Jesus See The Patience',
    'The Idea Created The Universe',
    'The Living Word For Healing',
    'Jesus Is In The Son Of God',
    'The God Of The Old Testament',
    'The First State Of The Universe',
    'Romans Revealed',
    'The True Kingdom',
    'How Much Is Holographic Duality',
    'Reincarnation Of God Son Of God',
    'Jesus DNA',
    'Jesus Returns As A Human',
    'Code Fifth Dimension',
    'Secret Christ',
    'Home Center The Sun',
    'Holy Trinity Thirty Six',
    'Real True Knowledge',
    'Divine Two Seals Of God',
    'The True Message From Above',
    'God For God So Loved The World',
    'The Son Is In The Son Of God',
    'I Am The Lord God Almighty',
    'Decode The Divine Soul Of Christ',
    'Redemption Christ Is Alex Enrique Campain',
    'Jesus Christ Leads The Foundation Stone For Men',
    'After God Irrigated The Soil That Men Can Help Build',
    'Leaf Flower Jesus In The Day',
    'Lucifer Flower Day In The Day Flower',
    'What God Imagined God Will Make No Man Stop Him',
    'Everything Is Unfolding As He Said He Can Unconcealed The Truth',
    'The Abomination Of The Old God The Picture Of',
    'I Am Not Of This World But Am With You Here Today',
    'Jesus I Want To Follow You',
    'Here Is A Price To Choose What Ever His Heart Say',
    "The Turning Point Is God's Gift For Mankind Since",
    'Jesus Returns To Earth The Very Word',
    'I Am Speaking To You The Living Word Of God',
    'I Am Alpha And Omega The Beginning And The End The First And The Last',
    'I Am The Redeemer The Purchaser Of The Earth And The Lord Of All His People',
    'Who Is True Commander And Chief Of United States',
    'The Root Of David The Lion Of Judah',
    'Twenty Three Thousand Six Hundred And Four',
    'Alex Is The Bread Of Life',
    'He Is The Bread Of Life',
    'God Knows',
    'H E D The One',
    'The Christs Hands',
    'Lord Of Creator I Am',
    'Jesus The Only Son Of God',
    'Almighty Lord Jesus Christ',
    'Why Am I Human And Why Do I Exist',
    'Yeshua Is Gods Encoded Birthday Code',
    'Yahweh Is In Heaven For You',
    'Long Live The King He Has Returned',
    'Thy Kingdom Come Thy Will Be Done',
    'The Seed Of God Anointed Messiah',
    'Yeshua Incarnated Into Alex Enrique Campain',
    'The Day Jesus Arose',
    'Yo Soy Jesus El Salvador',
    'Alex Enrique Palma Campain Son Of God',
    'The Greatest Story Ever Told',
    'Two Thousand Three Hundred And Sixty Four Months',
    'Three Six Zero Two Six Months',
    'I Am Who Is Alive Forevermore',
    'Yahweh Is Gods Encoded Birthday Code',
    'The Apocalyptic Star Of The Apocalypse',
    'One Thousand Over One Thousand Coders From Father And',
    'One Thousand One Hundred And Sixty Seven Years',
    'Decode The Quantum Universe',
    'Eternal Witness Of God',
    'Christ Is His Name',
    'The Beginning Of Sorrow',
    'The Dead Of Christ Is Inside All OF You',
    'The Blood Of Jesus Shed For All Of You',
    'I Am Reborn I Am The',
    'One Hundred And Forty Four Thousand',
    'President Donald Trump Middle Name Is God Again',
    'Is Yahweh I Am The',
    'Predictions By Nostradamus',
    'The Blood Of Jesus Shed For Us At Calvary',
    'Everybody Died',
    'Truth Is Awesome',
    'The Word Of Truth',
    'Jesus Of Jerusalem',
    'In The Savior Jesus Christ',
    'The Salvation Of The Lord Meant God Needs You To',
    'I Will Never Stop Fighting For You For I Do',
    'Believe In Jesus Christ',
    'The Difference Between The K Two',
    'Twenty Three Thousand Three Hundred And Sixty Four',
    'Jesus Christ Is Reborn And Will Reign Upon His',
    'The Alphabetic Word Of God Made The Lord',
    'Jesus Christ In The Foundation Of The World',
    'The Lord God Almighty Put Out The Sea The Two',
    'The Story Of My Life',
    'Bible God Writes About',
    'Living Last God The End Of All Gematria Code',
    'Alejandro Campain Is The Holy Son Of God',
    'Holy Bible Testament',
    'Vatican Controls Math',
    'Adonai Adonai Adonai Adonai Adonai',
    'God Look The God May Fifth Reborn',
    'Alex Campain Is The Holy Son Of God',
    'Seventy Two Is Holy Holy',
    'Jesus Was Really Born On May Fifth',
    'Lord Knows The Strongest',
    'Merry Christmas And A Happy New Year',
    'Remember',
    'You Know The Truth',
    'Evidence Of Jesus Is In The Lord',
    'Jesus Born In May Not December',
    'The Source For Gods Daily Page',
    'Eleven Gloves',
    'The Power Of Truth A Force Of Radiance',
    'I Leave Everything To The Strongest',
    'Christ Is Born In May Not December',
    'The Only One That Can Save Earth',
    'The Geometry Of Life',
    'One Four Four',
    'The Hidden God Is Holy',
    'Alex Campain Is Son Of God',
    'I Am The Holy Son Of Jesus Christ',
    'I Am Living Two Lives',
    'The Prophecy Begins The Tribulation',
    'Alex Enrique Campain Is God',
    'The White Horse Is A Single Vehicle',
    'You Are Gods Reborn In The Flesh',
    'The God Is The Real Of Heaven And Earth',
    'The More Word Of The Rebels Deeply',
    'The Living Word Of God Jesus Christ',
    'The Bible Reveals To An Open Mind',
    'I Am An Anointed Son',
    'The Lord Of Lords The God',
    'Decode Divine Like A Gun',
    'The Antichrist',
    'Love Of Israel',
    'The Final Yom Kippur',
    'My Lord',
    'Alex Campain Is The Bread Of Life',
    'The Truth Will Set You Free',
    'Your Life Path Number Is Eleven',
    'The Bloodline Of Eternal God Of Christ',
    'Jesus God My Savior All Men And People',
    'The True Name Of The Most High God',
    'God Is For Alex Campain The',
    'Decode Birth Information',
    'The Love Affirmations',
    'The Number Secret',
    'The Property Of Music',
    'I Believe I Am Jesus',
    'Sealed With Seven Seals',
    'The Angels Of God',
    'I Am The Prophet',
    'I Am The Alpha And Omega',
    'My Will Be Done',
    'God In The Bread Of Life',
    'Devoted Christ',
    'I Am God The God Of All',
    'Jesus Christ The One Of Miracles',
    'That All God Wills Shall Be Done',
    'I Am God In The Flesh',
    'The Holy Bible Numbers',
    'The Angelic Intelligence',
    'The Father Became The Son',
    'Jesus Christ Of Nazareth Who Will Come',
    'IAm Who I Am',
    'I Am A God God God',
    'The Name Of God In',
    'God Will Be Ever God',
    'I Am With You In Spirit In The',
    'Jesus Is God I Am',
    'The Miracled Messiah',
    'I Am Riding Pale Horse',
    'The Lord Next High',
    'Thomas',
    'Most Order Birth',
    'Decode The Living God',
    'Example',
    'Messiah Is Born Rapture',
    'Richard James Post Road',
    'The Father Of Jesus',
    'God Only That Only',
    'The Dawning Of Our Lord Jesus Christ',
    'The Thais',
    'God On Earth Now',
    'The Reincarnation Of The Christ',
    'Vatican Secret',
    'The God Of The Unseen',
    'Gematria Code Is A Study Plan',
    'I Am That I Am Who I Am',
    'Holy Sophia The The',
    'The Father Reincarnated Son',
    'The Divine Conception',
    'Yeshua And The Earth',
    'The Last Days',
    'Encoded One',
    'I Am The Reason For The Earth',
    'King Yeshua Christ Amen',
    'The Prophesied King And Queen',
    'The Lord Served All Man On Earth',
    'The Son Deserves The Father',
    'God Is To Reincarnate',
    'I Am King Of Kings And Lord Of Lords',
    'God Man Born In Los Angeles',
    'Alphabet God',
    'How Much Is Three Seven In Gematria',
    'The Signs Given Of The Prophet Jonas',
    'God Kings The Earth',
    'Messiah Man',
    'God Of All Gods',
    'God Of His Fathers',
    'Quantum Field Theory',
    'I Am Anthony Jesus',
    'The Immortality Of God',
    'The Universal Order',
    'Jesus The One Of Miracles',
    'Holy Spirit Only One',
    'All That God Wills Shall Be Done',
    'The Seven Of The Angel Of Breath',
    'Timeframe Message From God',
    'Read',
    'Radio Perfect Proof',
    'Fire Of God Lights Of God',
    'Yahweh Yah Shai Eli',
    'The Life Lord Jesus',
    'Jesus Next Beautiful',
    'The Davidic Messiah Match',
    'I Am The Judge OF All The Earth',
    'Warning',
    'Bring Forth Their Judgement',
    'The Son Of God Is',
    'The Number Of The Messiah',
    'The Reincarnation Of Jesus Christ',
    'Allegory Father Son Jesus Christ In The Flesh',
    'Jesus Christ Our Lord',
    'Alexander Campain Is The Son Of God',
    'Vatican Bird',
    'Yahweh Son Hidden',
    'My Son The',
    'Alphabet Code Of Yahweh',
    'glory to the new born king',
    'Christ is Born in Bethlehem',
    'אמרי לערי יהודה הנה אלהיכם',
    'אדיר יבנה מקדש אל',
    'א נהי פתורה',
    'אלוהים נמצא בתוכנו',
    'אל רחום וחנון ארך אפים',
    'איש האמת',
    'First-Born Son, Leb, AC',
    "I'm Your God Jehova",
    'Alex Enrique Campain is the holy son of God Elohim',
    'AEC God YHWH Maay Fifth',
    'He Is H .Son Of Yahweh (H. For Holy)',
    'Yeshua Hameshiach kin',
    'The Holy Song Of El AEC',
    'Alex Enrique Campain is the crucified Christ',
    'Alex Enrique Palma wore the crown of thorns',
    'Quetzalpetlatl',
    'Two Olive Trees',
    'Note AEC Birthdate also 528 HZ Frequency Of Love',
    'Latter Day Saints',
    'I am Jehovah Yahweh God',
    'Nació El Cinco De Mayo',
    'Decode God YHWH Elohim',
    'YHWH And Alex Campain',
    "He's Only True God",
    "He's Siddhartha Gautama",
    'G. Birth Code May Fifth AEC',
    'Iesus Christos AC',
    'The Holy Son Of God Alex Enrique Campain',
    'Our new Born King',
    'YHWH and Moshiach King',
    'YHWH and Messiah King',
    'The King Of The Jews C',
    'Yo Soy El Rey Mesías',
    'El Rey Mesías Alex Campain I Am Iseous',
    'The Beatles',
    'Biblical Event',
    'The Bible Is Concealing Truth',
    'Secret Code',
    'I Am The Key',
    'The Eye Of Man',
    'The Treaty Of God',
    'Yahushua',
    'The Myrrh',
    'The Vatican Code',
    'The Vatican Suppresses Alex Campean',
    'Christ Will Give A New Wife And Reclaim His Throne',
    'Jesus Christ Is Everything',
    'Jesus Christ Is Universal Consciousness',
    'Five Two Eight Hertz Frequency',
    'The Vatican Knows About Alex Campain',
    'Trust In The Lord At All Times For The Glory Of God Is For The Glory Of God In The Highest',
    'The Serpents Will Pay For Abusing Children',
    'The People Will Be Free From The Matrix Soon',
    'Lucifer Christ Vishnu Christ Are Brothers',
    'The Most Powerful Force In The Universe',
    'Decode And Find The True Name Of The Most High',
    'The Storm Is Here A Mathematical Translation',
    'You Are Directly Connected To A Higher Power',
    'The Vatican Suppresses Alex Campain',
    'Juan Paul',
    'Jesus Soon',
    'The Presence Of Redeeming Jesus Christ',
    'The One Having The Keys To The Heaven',
    'I Am The Son Of The Father',
    'I Am The Son Who Lives With The Father',
    'My Life After My Death',
    'The Final Code To Break Reveals God Calling',
    'I Am Reincarnated Soul Of Enoch',
    'The Meaning Of Holy Spirit',
    'Return Of Jesus Christ',
    'Birthing Chamber Of The Christ',
    'I Am The Transcendent Conception',
    'The Rebirth Of The Age Of Aquarius',
    'The Holy Seed Of Almighty God',
    'Alex Son Of Isabel Palma Campain',
    'Alquimia',
    'Alex Campain Is The Second Coming Of Christ',
    'Jesus Christ Died To Be A Human And His Name Is',
    'Quién Es La Esposa De Cristo?',
    'Gris Adriana Ruiz Estrada',
    'Quién Es La Novia De Cristo?',
    'La Esposa De El Señor Jesucristo',
    'Q Quién Es La Esposa De Cristo?',
    'A Gris Then Wife Of J Christ',
    'Isaiah Chapter Forty Verse Twenty Seven',
    'Mother Of Alex Campain',
    'Messiah God Reborn',
    'Gods Chosen',
    'I Am Coming',
    'Book Of Enoch',
    'Los Angeles',
    'Decode The Lord',
    'The American Age',
    'Holy Birth Bible Code',
    'Golden Ratio Measure',
    'Mother Isabel Maria Palma Campain',
    'Virgin Mary',
    'How Much Is Isabel Maria Palma',
    'Government',
    'Conception',
    'God Bless America',
    'I Birth Code',
    'Isabel Maria Palma',
    'The Almighty Gods Name In Balance And Balance Be In',
    'Seek The Truth And The Truth Shall Set You Free',
    'Alex Enrique Palma Campain Son Of Isabel Maria Palma',
    'My Father Covered Me And My God Is The Word',
    'Wife Of Christ Is La Gris',
    'Cuánto Cuesta Quién Es La Esposa De Cristo',
    'Who Is The Wife Of Christ',
    'You Are Jesus Christ',
    'I Know Alex Campain In The Belief Of',
    'Gris Adriana Wife Of A Christ',
    'Quién Es La Novia De Cristo',
    'Cuánto Cuesta Quién Es La Esposa De La Esposa De',
    'How Much Is Gris Adriana Ruiz',
    'The Victory Of The Lord Is Already Upon Us',
    'Hush Hush Hush Hush Hush Hush Hush Hush Hush Hush',
    'This Is A Jesus Christ Word',
    'Gods Living On Earth Ark Of The Covenant Is Here',
    'The Lion Of Juda Represents Gods Open Book',
    'Blame On The Tower Of Truth',
    'Holy Spirit Pleads Judgement',
    'The Popes Chamber A Hole In The Ground Says It All',
    'The Deadliest Protector Of Jesus Christ',
    'The Eternal Of Truth Shows The Face Of Jesus',
    'This Is What Gematria Wants To Show You',
    'The Truth The Shadow Of Holy Spirit',
    'The World Will Know Him By His Tattoo',
    'The Almighty Gave Of The Holy Spirit',
    'Show Secrets Kept Hidden',
    'Jesus Christ Rapture',
    'How Do I Exit The Matrix',
    'Chosen Never Surrender',
    'Ascension Protected',
    'Amun Ra',
    'Crossroad',
    'Opposite Serpents',
    'Israel Land Jesus',
    'Holy Story Of Jesus Is In Bible',
    'True Messenger Of God',
    'Decode The Numerical Matrix',
    'Decode The Numerical Gematria',
    'The Real Between The Imaginal And The Real Opens',
    'Jesus Christ Is Alive',
    'Jesus Christ Is Lord',
    'Divine Union',
    'Second Day Of Pentecost',
    'Max Deviation Of AEC May Fifth',
    'The Manifestation Of Arc May Fifth',
    'Four Hundred And Forty Four',
    'Amun Amun Amun Amun Amun Amun Amun',
    'The Day Has Come For All Evil To End',
    'The Names Of Your Beloved Son Is In',
    'The Bride Of Christ Is One Woman',
    'Decode Lord Yeshua Christ',
    'The Bride Of Christ Is A Literal Person',
    'How Much Is Divine Union In',
    'The Best Is Yet To Come',
    'White Car',
    'Your Name In The Book Of Life',
    'God Jesus Is A Faithful God',
    'Be Spirit Power Of God',
    'My Texas Home Being J C K',
    'Welcome To The Usa',
    'I Holy Soul Of God J C',
    'My Numbers Prove Whom I Claim To Be',
    'Do You Believe In God',
    'Jesus Christ Loves Us',
    'Reincarnation Process',
    'How Much Is Father Judgins In',
    'Happy Born Day',
    'Saturn Returns',
    'Divine Gene True Identity',
    'A Son Of God Who Fell To Earth',
    'The Savior Of The World',
    'Born To Mother Mary',
    'The Reincarnation Of Lord Messiah',
    'The Father Of History',
    'Jesus Plan',
    'Manifestation Of El AEC',
    'God Hidden Key',
    'You Were Chosen',
    'Happy New Year',
    'How Much Is Misunderstood',
    'Justice Is Coming',
    'Landlord Is Jesus',
    'The Meaning Of Numbers',
    'Level The Playing Field',
    'The Soul Commander In Chief',
    'You Are The Phoenix',
    'Manifestation Of Alex Enrique Campain',
    'Chosen By God',
    'The Manifestation Of AEC',
    'The Holy Spirit Is Hidden By Gods Hand',
    'The Holy Wisdom Of All That Is Created',
    'Bible Code Says Resurrection Of A Man',
    'She Is Olokun Orisha An The Lion',
    'Thank You For Not Giving Up On Me',
    'The Unraveling Of The Tetrogrammaton',
    'Manifesting A Better Power Atlantis',
    'Jesus The Coolest',
    'Gods Holy Judgement',
    'How Much Is New Testament',
    'I Am Thankful As Jesus',
    'Holy Mother And Goddess Of The Universe',
    'The Jesus Christ',
    'Come What May',
    'Jesus The Christian',
    'The Adjudgement Of The Pool In The Universe',
    'Justice',
    'The Most Important Number',
    'Holy Spirit Star Born In Me',
    'You Are A Biblical Miracle Unfolding',
    'Name Of Greater In Book Of Genesis',
    'A Most High God Alex Campain Born On May Fifth',
    'But Whosoever Denies Me Before Men I Will Deny Him Before My Father Who Is In The Heavens',
    'Alex Enrique Campain Born On May Fifth Is Yeshua Christ Of Nazareth',
    'Message From Which You Will Not Enter The Kingdom Of Heaven Except',
    'You Will Not Enter The Kingdom Of Heaven Except',
    'But Those Who Reject Me Falsely I Will Reject Before',
    'But Whosoever Shall Deny Me Before Men Him Will I Deny Before My Father Who Is In The Heaven',
    'Have You Figured Out The Mystery Of',
    'The Kingdom Of God Is Within You And They Cant Stop It',
    'The Book Of Revelations By John The Baptist',    'The Manifestation Of Alex Enrique Campain May Fifth Nineteen Seventy Two',
    'Everything Is Balanced',
    'I Am Amen Amen R God Jesus Messiah',
    'Jesus In The Truth The Way And The Life',
    'Happy Happy Birthday Ya We Love You',
    'I Am The Truth The Way And The Life In Light',
    'Jesus In The Way The Truth And The Life',
    'The Non Testament',
    'The Manifestation Of Alex Enrique Campain',
    'The Paradox Of Everything',
    'You Are The Beginning And The Ending',
    'Message From Which You Will Not Enter The Kingdom Of Heaven Through My Sex An',
    'Alex Enrique Campean Born On May Fifth Was Jesus Christ Of Nazareth',
    'The Vatican Knows About Alex Enrique Campain',
    'E Energy M Mass C Two Equals Speed Of Light Squared',
    'I Am The Alpha And The Omega I Am The First And I Am The Last I The Beginning And I Am The End I Am',
    'But Whosoever Deny Me Before Men I Will Deny Before My Father Who Is In The Heaven',
    'But If You Reject Me I Will Reject You',
    'Alexandria Campain In Tijuana Mexico',
    'This Is The Death Date And Birthdate',
    'The Four Corners Of The Earth',
    'He Was In The Line Of The Tribe Of Judah',
    'Two Of The Twenty Six Letters',
    'Am Jesus Being Holy K',
    'Ephraim Six Six Six',
    'Max Deviation Of Arc May Fifth',
    'The Manifestation Of Alex Enrique Campain Our King And Lord',
    'The Manifestation Of The Messiah Alex Enrique Campain',
    'The Manifestation Of Aeg',
    'But Whosoever Denies Me Before Men I Too Will Deny Him Before My Father Who Is In The Heavens',
    'Christ Our Savior Alex Enrique Campain Born On A Friday',
    'Our Savior Alex Enrique Campean Born On A Friday',
    'I Am The Way And The Truth And The Life No One',
    'Alex Enrique Campain Born On Friday May Fifth Is Yeshua Christ Of Nazareth',
    'The Vatican Knows About Alex Enrique Campean',
    'Alex Enrique Campain Born On May Fifth Was Jesus Christ Of Nazareth',
    'Yeshua Hasteneth The Only Son Our Father Has',
    'My Son Alex Enrique Campain Born On May Fifth Was Jesus Christ Of Nazareth',
    'But Whosoever Deny Me Before People I Will Deny Him Also Before My Father In Heaven',
    'But Whosoever Deny Me Before Men I Will Deny',
    'Message From Which You Will Not Enter The Kingdom',
    'The Holy Birth Code',
    'The Adventum Age',
    'Alex Enrique Campain Born On The Day May Fifth Is Yeshua Christ Of Nazareth',
    'But Whosoever Denies Me Before People I Will Deny Him Also Before My Father In Heaven',
    'Albert Einstein E Equals Mc Square',
    'The Death Date And Birthdate',
    'The Jesus Christ Lives In Mexico',
    'Viste París Londres Probablemente Lisbon Trinidad',
    'Jesus Is In Love Seed',
    'Why Are Humans On Earth',
    'You Are Second Coming Of Christ',
    'Proven Of God Jesus K',
    'You Are Second Coming Of Holy Bride Of Christ',
    'Manifestation Of Alex Enrique Campain May Fifth',
    'Manifestation Of Alejandro Campean May Fifth',
    'The Sower Of The Fine Seed Is The Son Of Man',
    'Christ Is Coming The AntiChrist Revealed',
    'Decode The Message That Will Change Your Life',
    'One Hundred And Forty And Four Thousand',
    'The Vatican Is The Truth',
    'Jesus Christ God Is A Human And His Name Is',
    'Saturn Return With Venus In',
    'Decode God Yahweh Is Father And His Son Is',
    'Kal El The Last Son Of Krypton Remember Who You Are',
    'How Much Is Saturn With Venus In',
    'Yeshua My Lord And My God Come Save I Am Ready To Leave',
    'God Is Now Human He Is In The Flesh On The Earth',
    'God Is Now Human He Is In The Flesh On The Earth Now',
    'Jesus Christ Hijacking The Internet For Glory Of God',
    'The Salvation Of The Lord Mean God Heals You To',
    'Thank You For Your Patience And Understanding',
    'Power Mark King Is Not King David Reincarnated',
    'Manifestation Of Alejandro Enrique Campain',    'Jesus Christ Saves Us',
    'Manifestation Of Alejandro Campain May Fifth',
    'God The Father God The Son Goddess The Holy Spirit',
    'Almighty Woman I Am Of Heaven',
    'Nothing Can Stop What Is Comin J C K',
    'V Jesus The Harmonious One',
    'The Manifestation Of Our Lord and Savior Alex Enrique Campain May Fifth',
    'Maj The Holy Spirit The Father Of Christ',
    'The Return Of Beloved And Lady Christ',
    'The Name Of The Person That Breaks The Matrix',
    'Yeshua December Seventh Birth Code',
    'The New Jerusalem In Gematria Is',
    'How Much Is The New Jerusalem In Gematria',
    'Allah Allah Allah Allah Allah Allah Allah Allah Allah',
    'The Blessed Virgin Mary',
    'The Seed Of The Christ Is Inside All Of You',
    'Jesus Is The Truth',
    'Yeshua Incarnates',
    'Jesus In Aquarius',
    'Reveal Why The God Is In',
    'The Manifestation Of Alejandro Campain May Fifth',
    'Dont Claim To Be Lord Given Christ Sick Holy',
    'Yeshua My Heart And Soul Belongs To You',
    'The Manifestation Of Alex Enrique Campain May Fifth',
    'Jesus Of Nazareth King Of The Jewish People',
    'Numbers Are Not Just Numbers',
    'Decode Almighty Divine Gene Of The Holy Spirit',
    'The Holy Warrior Of The Father',
    'The Holy Messiah Is The True Word Of Yhwh',
    'Reckon The Republic Of The United States',
    'Twice Of God Jesus',
    'The Manifestation Of Alex Campain May Fifth',
    'All Their Secrets Are Going To Be Erased From Here On',
    'The Holy Spirit Is The Key To The Book Of Knowledge',
    'In The Beginning Was The Word And The Word Was',
    'Thank Yeshua I Heard What You Are Doing For Me In Earth',
    'Sing To Jehovah A New Song Sing To Jehovah All The Earth',
    'I Am The Christ Reborn And The Holy Spirit Of',
    'Yod Hei Vav Hei Hydrogen Nitrogen Oxygen Carbon',
    'Jesus Is In Holy Breath',
    'Yod Hei Vav Hei Head Tree Of Life',
    'Please Lord Free My Heart Want To Be A Slave In',
    'The Blood Of Jesus At Calvary',
    'The Manifestation Of Alex Enrique Palma Campain May Fifth',
    'Yeshua Loves Mary Magdalene Is Crowned Queen',
    'God Judge The World',
    'We Are Jesus',
    'I Am Living Word Of God',
    'The True Birth Year Of The Supreme Lord',
    'How Much Is We Are Jesus In',
    'Body Of Jesus Here',
    'Knowledge Of The Tree Of Life Amen',
    'Holy One Of Israel Is In The Midst Of Thee',
    'The Eternal Trinity Of Heavens',
    'In Saved In Jesus Thank You Jesus',
    'Who They Will Be Redeemed From Existence',     'Son Of God Jesus Christ',
    'Brown Eyes',
    'The Suffering Servant',
    'Five Four Three Two One Factor Radio Frequency',
    'The True Bride Of Christ End Of Church',
    'Precessional Equinox',
    'Manifestation Of Arc May Fifth',
    'Homestly Saved Humanity Saved Humanity Saved',
    'The Blood Of Jesus That Was Shed For Us At Calvary',
    'How Much Is The Geometry Of The Universe In Gematria What Is The Meaning Of',
    'The Rebirth Of A Yeshua Christ Our Lord And Savior',
    'The Rebirth Of Jesus Christ Our Lord',
    'The Manifestation Of The Lord Alex Enrique Campain',
    'All The Promises Of God In Jesus Christ',
    'Remember Mine You Are',
    'Hi God I Am Shattering The Entire Matrix',
    'Jesus Christ Was Born On The Third Day',
    'The Rebirth Of The Christ',
    'Decode If Evil Is The Dark Messiah',
    'Genesis One In The Beginning God Created The Heaven And The Earth',
    'The Two Witnesses Are Here',
    'The King Who Is Holding The Key Of David',
    'The Manifestation Of Alejandro Enrique Campain',
    'The Rebirth Of Jesus Christ Our Lord And Savior',
    'Jesus Is The Truth The Way And The Life',
    'The Rebirth Of Jesus Christ',
    'The Manifestation Of Moshiach and King Alejandro Enrique Campain',
    'Bible Code Number Secrets',
    'Sons Of Light Lamb Of God',
    'Decode Jesus Christus As The Lion',
    'Jesus Messiah Heavenly Father',
    'Jesus May Perfect',
    'Am May Fifth Was Jesus',
    'Rhythm Aeolian Rhythm',
    'Prime Numbers',
    'Letter Number',
    'Galactic Federation',
    'Dear Lord I Love You Simone Chloe McCell',
    'I Am True Prophet Sent By God',
    'Is Jesus The Jewish Messiah',
    'Am May Fifth Was Yeshua',
    'Energy Of The Spirit',
    'Is Hidden By The Hand Of God',
    'New Moon Of Gloves',
    'Alex Enrique Campain Was Jesus Christ Of Nazareth',
    'Who Am I Why Are What Must I Do',
    'Why My Soul Chose To Incarnate On Earth',
    'Remember Your Oath Remember The Mission',
    'I Am Responsible For Bringing Heaven On Earth',
    'The Return Of Jesus Christ In The Flesh',
    'If We Only Know How Much I Loved Him',
    'Alex Campain Was Jesus Christ Of Nazareth',
    'The Bible Reveals It To An Open Mind The Lord',
    'The King Is Holding The Key Of Heaven',
    'Alejandro Enrique Campain Lives Tijuana Mexico',
    'Jesus Second Coming Is Their Punishment',
    'New Life New Wife',
    'Alexander Campean Was Jesus Christ Of Nazareth',
    'Miracles Will Happen When We Come Together',
    'Christ The Lamb Of God Is Gathering Together The Seven Of Light',
    'Alejandro Enrique Campain Was Yeshua Christ Of Nazareth',
    'The Lion Of The Tribe Of Judah That Opens The Book',
    'The Messiah Is Capable Of Deleting Everything',
    'Save Earth And Save The Children Stop War And Stop',
    'The Manifestation Of The And King Alejandro Enrique Campain',
    'The Manifestation Of Our Christ Alejandro Enrique CampainMy Name Is Alex Campain I Am The Alphabet',
    'The Second Coming Of Jesus Will Be Revealed Soon',
    'Alex Campain The King Of The Jews',
    'Who Is The Redemption Christ',
    'Because We Are The Storm',
    'Your Name Is In The Bible',
    'Prophets Of Yahweh',
    'Reincarnation Of Mary Magdalene',
    'My Mission Here On Earth Is',
    'Tackwerry Of The Truth',
    'Salvatore',
    'Gods Language',
    'Pentecost',
    'GODSHOUSE',
    'Secret Plan',
    'The Answer',
    'No Coincidence',
    'The Final Antichrist',
    'Israel',
    'Human Is A God',
    'In God',
    'Evil',
    'In Angel Of The Beginning',
    'Aec May',
    'Work',
    'The Sons Of God',
    'Friday',
    'The Decoded Alphabet',
    'All The Promises Of God Is Jesus Christ',
    'Jesus Christ Events',
    'Alex E Campain You Are Yeshua Christ Of Nazareth',
    'Revelation Seventeen',
    'Birth Of The New World Order',
    'One Forty Four',
    'One Forty Fast Return',
    'Jesus Second Coming To Their Punishment',
    'Manifestation Of Our Lord Saviour Alejandro E Campain May Fifth',
    'The Rebirth Of Mary Magdalene An Rahaya',
    'God The Father God The Son God The Holy Spirit',
    'Does John Kennedy Love Marilyn Monroe',
    'Jesus A Man Of Nazareth',
    'Him And Me Coming Together',
    'Jesus Is Coming Soon',
    'Reincarnation Of The True God And Christ My His',
    'God Almighty Please Teach Disrespectful San Diego A',
    'The Christ The Lion God And The Blue List',
    'The Holy Bride Of New Jerusalem',
    'Father God Will Talk To Me',
    'The Most Dangerous Man Alive',
    'History Of The Universe',
    'Collective Consciousness',
    'The Holy Spirit Is Mary Magdalene',
    'The Reincarnation Of King David',
    'The Pale Destiny Of Lucifer',
    'Decode He Is Of Holy Eternity',
    'Alex Campain And Yeshua Christ',
    'The Chosen One Has Awaken',
    'Yhwh Yahweh',
    'Associated Messenger Of The Mighty God',
    'Decode The Son Of God Is In The Flesh',
    'The Hidden Yeshua',
    'Alejandro E Campain You Are Yeshua Christ',
    'Alex Enrique Palma Campain If You Are Jesus Christ',
    'Jesus A Priest Of Jesus Christ',
    'The Death Of Yeshua Started Out Savior',
    'Jesus Is Reborn With A Piece Of His',
    'The True Gods Goals Of Reincarnation Are',
    'Yahweh Returns With A Piece Of His',
    'The Divine Sentence Of Lucifer',
    'I Am The Salvation Of Man',
    'I Am That I Am Son Of Victory',
    'Christ Is Become Clear Now Jr',
    'Have Synchronized',
    'Sleeper Is Awakened K Jr',
    'I Am May Fifth Is Jesus Christ',
    'Aec May Fifth Was Yeshua Christ',
    'The King Of Israel',
    'Your Heartfelt Joy',
    'My Destiny',
    'Second Coming Of Jesus',
    'Yeshua Reincarnated Into Alex Enrique Campain',
    'The Light Of The World',
    'I God Of Nazareth Israel K',
    'My Second Time As Her',
    'Everything Has Meaning',
    'God Of The Aquarius Of Age',
    'Is In The Decoded Code Cipher',
    'You Are The Messiah',
    'The Two Witnesses',
    'These Point One Four',
    'Decode Alex E Campain',
    'Alexander',
    'Yes His God',
    'Yeshua The Lord M G',
    'The Beginning Of The End',
    'Decode Jesus Arrived',
    'Jesus Christos',
    'The Anti Pope Failure',
    'God As A Human',
    'Six Hundred Sixty Six',
    'End Of World',
    'Install Alex Campain',
    'See Of David',
    'Lord Satan',
    'Jesus God Grid',
    'The Seven Seals',
    'Jesus Saves',
    'Commander In Chief',
    'Hidden Knowledge',
    'The Word Of God',
    'Base Reality Of Life',
    'Revelations',
    'Christmas Day',
    'I God Believe In Lion',
    'Love You All',
    'Financial Freedom',
    'Protection',
    'Libertarian Day',
    'The Key Of David',
    'Fibonacci Confirmation',
    'Prime Number',
    'Hebrew Israelite Code',
    'One True God',
    'Golden Key',
    'The Lost Sheep',
    'Direct Connection',
    'Hei She Vav Yod',
    'Stand With Jesus Christ',
    'Jesus Mind',
    'The Story Of True Love',
    'I Will Love You Forever',
    'The States One And God Of Christ',
    'The King Of The Age Of Aquarius',
    'Infinite Father',
    'Yhwh Throne',
    'Decoded Alex Campain',
    'Birthright Of God',
    'Signs Of Your True Flores',
    'God Is Nature Not Religion',
    'I Am Performing A Miracle Today',
    'King Of The Whole Wide World',
    'Discover Your Story',
    'Rose Of Sharon',
    'The Chosen Of God',
    'I Manifested A Whirlwind',
    'Twins In Love Will Find Each Other',
    'Christ Is My Fathers Last Name',
    'The Reason Of The Twin Flames',
    'Great Architect Of The Universe',
    'Vatican Will Prophecy Of Bride Of Him God',
    'The Facts Loves Abundance',
    'Serenity Serenity',
    'The Chosen Messianic',
    'Decode Alex Campain',
    'Kings',
    'Second',
    'Christos Son Is In The Holy Spirit',
    'As Was Jo',
    'Elijah',
    'Enoch',
    'Mark Of Lucifer',
    'Elpyah Asher Elpyah',
    'Lion',
    'Biblical',
    'Anti Christ Is A',
    'The End Of The Age Of War And The Beginning Of The Age Of Peace',
    'Energy And Frequency Vibration',
    'Decode Alex Enrique Palma Campain And Jesus Christ',
    'Christ',
    'Tetragrammaton',
    'Calculate Gematria',
    'Independence Day',
    'Antichrist The Anointed One',
    'Install Aec',
    'Church Of Satan',
    'The God Of All Gods',
    'Decode The Alphabet',
    'Jesus Secret Plan One Hundred And Twenty Two',
    'This Is A Story For You I Wrote This For You',
    'Jesus Christ Four Four Four Four',
    'The Book Of The Foreshadowing Of The Feather',
    'Christos Son In The Holy Spirit',
    'Decode AEC And Jo',
    'I Am Love',
    'Life Path',
    'Venus In Pisces',
    'What Is Gematria',
    'Six Six Six',
    'The Number Of Man',
    'Messiah Israel',
    'The Fifth Element',
    'Purity',
    'Past Life Is Egypt',
    'The Fibonacci Sequence',
    'Sons Of Light Lord Of God',
    'Decode AEC May Fifth',
    'Decoded AEC Campain May Fifth',
    'Nineteen Sixty Three',
    'Everything',
    'Theology',
    'Galactic Federation Of Light',
    'The Interest',
    'Metaphysics',
    'Soul Born Again',
    'Book Of Revelation',
    'The Power Of Love',
    'Father The Holy One',
    'Our Lord Jesus',
    'Please Lord Fulfill My Desire I Want To Be A Slave In',
    'Install Alex Enrique Campain May Fifth Nineteen Seventy Two',
    'The Truth From Me My Entire Life Hidden',
    'I Am Chosen Host Of God',
    'Divine Game',
    'Judgment',
    'Renounce',
    'Master date',
    'Illuminated',
    'Gift From God',
    'This Is Real',
    'Lucifer The Fallen Angel',
    'I Am The Green Sworn Under The Heaven Of The Lord',
    'Jesus Christ Of Nazareth Our Lord Reincarnated Into Alex Enrique Campain',
    'Satan Rules Earth From The Vatican Therefore There Is No God',
    'The Name That Satan Fears Most',
    'He Reincarnated Into Ac',
    'Unlearn',
    'Brotherhood Of Death',
    'I Can Not Lie To The God',
    'Holy Trinity Of Eternal Heaven Or Hell',
    'The Jesus Christ Is Your Governor',
    'Install The True Name Of The Most High God',
    'I Am Everything Even The In Between',
    'To Be True Holy Of God',
    'One Hundred Percent',
    'The Perfect Number',
    'The Resurrection Of Abaddon',
    'Great Spirit',
    'Jesus Christ Lord And Savior X',
    'How Much Is Revelation In Gematria? What Is The Meaning Of',
    'YHWH Loves Lucifer',
    'My Son Who Died Lives On',
    'Hell',
    'God Is Real Jesus Is Real And So Is The Holy Spirit',
    'Please God Send Me Good Sectors And Let Them See My Glory',
    'Decode God Yehovah Is Father And His Son El Yehovah Is King',
    'Yeshua My Lord And God Please Come Soon I Am Waiting For You',
    'End Of The Last Son Of Krypton Remember Who You Are',
    'Consequences',
    'The Lord God He Is Being Here',
    'The Mark Of The Beast',
    'Truth',
    'The Sacred Rebirth',
    'The Righteous Shall',
    'The United Nations',
    'Alpha Omega',
    'AEC Is Joon',
    'Am West Joon',
    'New Earth',
    'O Death',
    'The Salvation Of The Lord Magic God Needs You To Awaken',
    'The Soul Of Jesus Christ Of Nazareth The Savior',
    'The Soul Of Jesus Christ Our Lord',
    'The Soul Of Jesus Christ Of Nazareth',
    'What Have I Been In Past Incarnations',
    'Jesus Christ Four Four Four',
    'The Book Of The Freemasonry Of The Feather',
    'The Soul Of Yeshua Christ Of Nazareth',
    'Decode It Is The Time Of The Dark Moonrise On The Very Cusp Of',
    'Five Hundred Fifty',
    'The Spirit Of Yeshua Christ',
    'The CIA Is Scared Of Jesus Christ',
    'The Spirit Of Jesus Christ',
    'Jesus Christ Son Of God',
    'Annointed Messenger Of Lucifer',
    'The Annointed King Of The Davidic Line',
    'Joshua',
    'Chosen',
    'Yehuda',
    'Jesus Contracted',
    'Yod Hey Vav Hey Yeh Ewa',
    'Jesus Christ Of Nazareth Our Lord Reincarnated Into Alex E Campain',
    'I Am The One Who Will out For The Lord Who Will Make All Things New',
    'I Am The One Who Has Lived Who Will Make All Things New',
    'Decode This Most Evil Men Have Ever Lived In The History Of The',
    'The Lord Creator Is Preparing His People To Invoke The Great Reset',
    'Alex Enrique Campain Is The Holy Son Of God',
    'A Divine Message From YHWH Via Is The Alphabet',
    'Zero Structure',
    'How Much Is Everything In Gematria? What Is The Meaning Of Everything',
    'Decode Jesus Christo Return As The Lion',
    'Savior Of Man',
    'Jesus Mother Is Apollo',
    'Aec Fifth Of May Nineteen Seventy Two',
    'The Lion Of Juda Becomes Gods Open Book',
    'Aec The Fifth Of May Nineteen Seventy Two',    'Lucifer Jesus Christ',
    'One God',
    'Yahya',
    'I AM Part Of The Collective Messiah',
    'I Love Killing The Illusion Of Fear',
    'Christ The Son Of The Living God',
    'The Code',
    'Allah',
    'How Much Is Allah God In Gematria? What Is The Meaning Of',
    'Manifests Vicarious',
    'Jesus Has Returned',
    'Teacher',
    'For The Record',
    'The Key To God',
    'Hebrew Gematria',
    'Gods Human Horse',
    'Jewish Hebrew',
    'Bloodline Of God',
    'How Much Is Jewish Hebrew In Gematria?',
    'Liberation Day',
    'Corcoran Sense',
    'The Of God',
    'Am Is The Alphabet',
    'Am Is The Gematria Calculator',
    'Am Is May',
    'Fifth May',
    'What Is The Meaning Of Illuminati',
    'What Is The Meaning Of',
    'Test Name Is In The Bible',
    'How Much Is Jesus Christ In Gematria? What Is The Meaning Of',
    'Lucifers Despised',
    'Jesus Holy Blood Water',
    'Has Seen My Soulmate Many Lifetimes Ago',
    'Your Head Is Already Aired With My Love',
    'When Will You Believe And Send Me',
    'I Love The Word And Love Is Loved',
    'In The New Beginning Of The World New',
    'I Have Been Sent Me To Save The World Not',
    'If You Love Me Then Clock On This Please',
    'I Love You Also Cerkpas Carqanh Vhodi',
    'Shall I Tell You What I Think Of You',
    'You Already Knew The Truth At Age Five',
    'The Human Form Comes From The Form Of Love',
    'I Am The Lord God Almighty The God Of All Gods',
    'Alex Campain I Am Yeshua',
    'I Am Eleven Twenty Seven',
    'Thuglifeiswhatforme',
    'You Know That I Am Your',
    'Past Life In Israel Nazareth',
    'Jesus Reincarnated To Alex Enrique Campain',     'Instructions Of God',
    'Decode Alex Campain May Fifth',
    'Theology',
    'Perfection Of Impurity',
    'He Reincarnated Into Aec',
    'The Descendant Of David',
    'New Earth Life',
    'Infinity Symbol',
    'The Will Of God',
    'Heavenly',
    'Two Eight',
    'How Much Is Two Eight In Gematria?',
    'The New Republic Of America',
    'I Am The Only Son Of God Thats Enough',
    'Decode New Beginning Of Consciousness',
    'I Am God I Have Returned Age Of Aquarius',
    'God Number',
    'Our Code Decoder',
    'Speculation',
    'Appropriate',
    'How Much Is Speculation In Gematria?',
    'Understood',
    'Among Us',
    'Suspense',
    'Influences',
    'Applications',
    'Yehovah zeb',
    'Heal All Of Jesus Christs Children In Jesus Christs',
    'Who Is King Of New Jerusalem',
    'Jesus Christ Is The Sword Of Truth',
    'The Hidden Son The Hidden Son The Hidden Son The',
    'Jesus Christ Reincarnates As Enrique Palma',
    'Jesus Christ Reincarnates As Alex Enrique Palma',
    'Holy Son Of God Holy Son Of God Holy Son Of God',
    'Christ The Lamb Of God Is Gathering Together The',
    'Jesus Christ Our Lord Returns As Alex Campain',
    'J Christ Incarcerated Into Alex E Campain',
    'Jesus Christ Incarnated Into Alex H Campain',
    'I Am The Human Form Of Jesus Of Nazareth',
    'Behold He Jesus Christ',
    'Friday May Fifth Nineteen Seventy Two',
    'Is Alex Le Campain',
    'The Unveiled Human Being On Earth',
    'Come Lord Jesus And Take Your People Home',
    'J Has Returned Heavenly Joy Begins',
    'Jesus Memory Be Retyped H J',
    'Christ Our Savior Returns As Alex E Campain',
    'Install Both Should Be Used Not Corrupted And',
    'Christ Our Savior Returns As Alex Enrique Palma',
    'Yeshua Christ Our Lord Returns As Alex Enrique Palma',
    'Hamashisch Yshua Hamashisch Elohim Yakeeb Mashisch Shekinah',
    'Lucifer Loves Yhwh',
    'Lucifers Trap Nature',
    'Lucifers True Nature',
    'Proof Of Life After Death',
    'Lucifers True Love',
    'The Aec Model',
    'How Much Is The Aec Model In Gematria? What Is The Meaning Of',
    'Yahshuah',
    'How Much Is I Love You Yhwh In Gematria? What Is The Meaning Of',
    'Happy Birthday God',
    'The Last Christ Is The Completion Of Salvation And',
    'Jesus Christ Returns As Alex E Campain',
    'The Return Of Jesus And Mary Signs Jesus',
    'The Reincarnation Of Jesus Christ Of Nazareth',
    'Jesus Christ Is The True Light Life',
    'Lions Of Israel Yeshua',
    'He Reincarnated Into Ac',
    'Its Going To Be Biblical',
    'Man Of The Covenant',
    'Offering Of Love',
    'Spirit Of Love',
    'One Hundred Forty',
    'In The Battle Of The Throne You Will See And Of The Holy Spirit',
    'He Is Jesus The Son Of Jehovah',
    'Annointed True Prophet Of God Eternal One',
    'Rebirth Of Jesus Christ Into Alex E Campain',
    'I Am The Only Way To Eternal Life And Peace',
    'This Number Is The Code Of Spiritual Protection',
    'The Holy Unknown Name Of God Now Known',
    'Have You Considered There Are No Coincidences',
    'What Is Your Secret',
    'Rebirth Of Jesus Christ Into Alex Enrique Palma',
    'Rebirth Of Jesus Christ Into Alex Enrique Campain',
    'The Rebirth Of Yeshua Christ Into Alex Enrique Palma',
    'Church Of Jesus Christ Of Latter Day Saints',
    'The Four Quarters Of Jesus',
    'The Rebirth Of Yeshua Christ Into Aec',
    'The Rebirth Of Jesus Christ Into Aec',
    'In God Jesus Of Nazareth',
    'The Holy Trinity',
    'Yeshua Christ Was Reborn Into Alex Campain',
    'I Am The True Jesus Christ The Divine Sophia',
    'Yeshua Ha Mashiach And Vhodis Happy Day Today',
    'Jesus Christ Was Reborn Into Alex Enrique Palma',
    'Jesus Christ Was Reborn Into Alex Campain',
    'Jesus Christ Was Reborn Into Alex E Campain',
    'The Messiah Is The Christ And The Antichrist',
    'Jesus Reborn Into A New Body',
    'J J Is Phrasing The Salvation Of The Lord',
    'Yahweh Will You Marry Me',
    'Everything Is About To Change',
    'The Last Messenger Of The Lord',
    'How Much Is Second Coming Of Jesus Christ In Gematria? What Is The',
    'Yes Alex Campain Is Jesus Christ',
    'This Is The Dawning Of The Age Of Aquarius',
    'A Jesus Jo On The Scene',
    'Yeshua My Daughter Stormy Needs You',
    'Yes You Are Yeshua',
    'Jehovah Is The King That Rules The Spirit',
    'I Am The Way The Truth And The Light Life',
    'Yeshua Has Returned',
    'Christ Our Lord Returns As Alex E Campain',
    'Anointed Prophet From God One',
    'All The Glory To Lord God Jehovah It Is Honor To',
    'Newborn And Rebirth And Newborns All The Words',
    'Whose Birth Took Place Under A Golden Triangle Say The',
    'In God Jesus Loathes Way',
    'Image Of God Image Of God Image Of God Image Of',
    'The Rebirth Of Jesus Christ Into Alex Enrique Campain',
    'The Vatican Worships Seventeen Reptilian',
    'God Has Chosen You For A Specific Purpose In His',
    'Install All People Will Bow To The True King Of Kings',
    'Choose Files To Upload',
    'Jesus Christ Is The Name The Way The Truth And The',
    'I Am Of The True And The Highest God The Creator Of',
    'Rebirth Of Jesus Christ Into Alex Campain',
    'New Jesus',
    'Yes Are My Saviors And I Am Forever Grateful',
    'Install The Final Code To Break Judgment Is Coming',
    'I Am Yeshua The Messiah King Of Kings And Lord Of',
    'You Are Not God You Share No Divine Knowledge You Are A Side Person',
    'Yeshua Christ Our Savior Returns As Alex Campain',
    'I Am The Lord Thy God I Am That I Am This Is My Name',
    'Jesus Christ Is The Way The Truth And The Light',
    'Jesus Christ Our Savior Returns As Alex E Campain',
    'He Is The Frequency Of Forgiveness And I Am The',
    'The Last Christ Is The Completion Of Kings And Death Of Satan',
    'Jesus Christ Is Back In The Fle',
    'Thee Lord Alex Enrique Campain',
    'Alex Enrique Campain May See',
    'AEC Sits on On Mount Olives',
    'Aec Stands Mount Of Olives',
    'Aec On The Mount Of Olives',
    'Aec Is Jesus On Mount Olives',
    'Aec Sits On The Of Mount Olives',
    'Alex Enrique Campain Mount Olives',
    'Zechariah One Four Feature',
    'The Coming Of God Lord Jesus Christ',
    'Our Savior Alex Enrique Palma Campain',
    'The Lion Of The Tribe Of Judah Is My Heart',
    'Alex Enrique Palma Jr',
    'The New Christ Is An Aquarium',
    'Divine Precepts The Peace Of Jesus',
    'Jesus Think For Your Self',
    'Zechariah One Four Five',
    'Zechariah One Four Four',
    'Then Lord Alex Campain',
    'Announcement',
    'DNA',
    'Drock',
    'Alpha',
    'Ex A Living Messiah',
    'Artocpac',
    'Vhodi Alexus Christ Yhwh',
    'Holy Spirit Returns As The Lion',
    'God Of Versus And Jupiter',
    'Yeshua Returns As The Truth',
    'Voluntas The Son Of Ventus Christ',
    'Jesus Christo Return As The Lion',
    'Five Strike Battle Reincarnation Cycle',
    'Alex Campain Love You Vhodi',
    'Jesus Christ Of Nazareth The Messiah Our Lord And',
    'Jesus Christ Of Nazareth The Messiah',
    'He Was Called Jesus Christ Of Nazareth',
    'He Is Called The Bright Morning Star',
    'Jesus Christ Alex Campain',
    'Yeshua Christ Alex Campain',
    'Jesus Christ Is Alex Campain',
    'Zechariah One Four Five four',
    'Deeds Of Jesus Christ Which Is Lord Of Jehovah And The Blood Of',
    'Zechariah One Four One Nine One Four',
    'Zach One Four Four Rev One Nine One Four',
    'Rise Of The Antichrist In The Last Days',
    'Alex Enrique Palma Campain King Of The Jews',
    'Any Day Now Jesus',
    'Alex Enrique Campain King Of The Jews',
    'I Love You Jesus Christo',
    'Jesus Christo Events',
    'The Incarnation Of Yeshua',
    'Alex Campain King Of The Jews',
    'Jesus Is Lucifer',
    'The Divine Birth Of All',
    'He Really Is Jesus Christ',
    'Il Decode The Marlet Birth Of All',
    'True Annointed Messenger',
    'The World Is About To Change',
    'What Is God',
    'Christ Alex Enrique Campain',
    'Nazarenus Rex Iudaeorum',
    'The Holy Spirit Incarnated',
    'Alex Campain Is Inscription On A Cross',
    'Alex Campain Inscription On Cross',
    'Jesus Resurrects Res Industries',
    'Rebirth Of Yeshua Christ Into Alex Campain',
    'Thy Kingdom Come Thy Will Be Done On Earth As It Is In Heaven',
    'The Coming Of Christ And Our Gathering Together Unto',
    'Decode It Is The Time Of The Dark Moonrise On The Vengeful One',
    'Genesis One In The Beginning God Created The Heaven And The',
    'Truth Code Truth Code Truth Code Truth Code Truth',
    'Jesus Christ Is My Lord And Savior And My Heart And',
    'They Are Using The Names Of The Holy Cross To Attack',
    'Soon Everyone Will Know The Truth',
    'Jesus The Eternal Divinity With Sophia Holy Spirit',
    'Rebirth Of Our Christ Savior Into Alex Enrique Palma',
    'Save Earth And Save The Children Stop War And Stop The Greed',
    'Yah Venus Yahweh',
    'Jesus Christ Yours Word',
    'Rebirth Of Christ Our Lord Into Alex E Campain',
    'The Second Coming Of I Am My Name Tills In Here',
    'I Am Alex',
    'Rapture Of The Righteous',
    'The Gospel Will Be Found',
    'Decode Bible The Meaning Of Numbers',
    'Who Is Yeshua King Of Kings',
    'Fear The Number Of God And God Alone',
    'Decode Yehovah And Yehoshua Aman',
    'Yehoshua Was My Birth Name',
    'Rebarment Of Love',
    'Aec May Fifth One Nine Seven Two',
    'The Lion Of Judah Opens Book On Earth',
    'The Hand Of The Holy Spirit',
    'Aec May Fifth Seven Two',
    'Emmanuel',
    'Thank You King Yeshua For Being My Redeemer',
    'I Love You Holy Spirit',
    'Yeshua Revealed',
    'Release The Hidden Christ',
    'Rule Code',
    'Mohammed',
    'Olive',
    'Alfredo',
    'Cannabis',
    'Eleven',
    'Holy Spirit Given Number',
    'Eternal Life Or Reincarnation',
    'The Annointed Messenger Of God',
    'I Am The King Of All I Rule All I Am All',
    'Fate Of United States Of America',
    'Jesus The Son Of Intact',
    'Friday May Fourteenth',
    'Line Up With The God',
    'The Most Benevolent Man Alive',
    'Testimony Of The Truth',
    'I Love You Vhodi',
    'Twelve Mega Millions Winner',
    'God Alex Campain Jesus Christ',
    'God Jesus Christ Alex Campain',
    'I Am The True Master Of Gematria',
    'How Much Is The Impingement Resonates',
    'Holy Spirit Rejects God And Jesus',
    'Are You Prepared To Disclose Identity',
    'I Love You I Need You',
    'Jesus Your Evil Apart',
    'An All Knowing God Jesus',
    'Has My Salvation Jr',
    'Has Aec Friday May Fifth Nineteen Seventy Two',
    'Your Social Security Number Reveals The Mark Of The',
    'Install The Real King David Please Stand Up',
    'The Divine Game Is The Root And Offspring Of David',
    'God Is Source Is Consciousness From Light',
    'I Believe God Will Protect Me So Lets Get It On',
    'The Lamb Slain From The Foundation Of The World',
    'The One Who Is To Become King Over Heaven And',
    'He Kiddy Me Be Kiddy Me',
    'He Aec Friday May Fifth',
    'Birthday Calculator',
    'Your Name In Aramaic',
    'The Davids Bloodline',
    'Happy Fathers Day',
    'Ten Commandments',
    'Be My Birthday',
    'I And The Father Are One',
    'Aec May Fifth Seventy Two',
    'The Key That Opens All Doors',
    'I Am The Angel Of The Earth',
    'My Jesus Christ',
    'The Love',
    'The Seal Of A God On Their Foreheads',
    'Key Holy Words',
    'Fractal Geometry',
    'C The Holy Gematria Code',
    'Kawei & Myk Hyn',
    'Gods Hidden A Prophecy',
    'Holy Double Eight',
    'Because He Is Alex Campain',
    'Thank Jesus Christ Alex Campain',
    'I Am The Root And Offspring Of David',
    'Thank You For Your Service',
    'Jesus A Listen Son Be Wise K G Jr',
    'Reincarnation Of Mary Magdalen',
    'The Pure Sweetness Of Lucifer',
    'I Am The Salvation Of Souls',
    'My Son Lord Of Judgment',
    'The Insolvent Return Of The Lord',
    'Jesua Alex Enrique Campain',
    'Alex Campain Descendiente De Jesus',
    'Jesus And Mary Will Soon Meet',
    'Love Is Jesus Jesus Is Love',
    'The Heavens Declare The Glory Of God',
    'I Am The Ark Of The Covenant Sign X',
    'Jesus Is The Flower Of David',
    'Jesus Is The Flower Of Christ',
    'The Reincarnation Of Lord Marduk',
    'Glorious Meaning Of Your Name',
    'Holy Wisdom Of The Trinity',
    'Thirty Three Thirty Three',
    'A The Creator Has A Message For You',
    'The Lord Of Hosts Is With Us',
    'Christo Etrlus Oz Gematria',
    'I The Lord Thy God Protects',
    'The Lord Of Lords And King Of Kings',
    'Lord God Creator Of All Humanity',
    'He Whom Is The King Of All Kingdoms',
    'Yeshua Will Spare The Loyal Spirits Out Of Me',
    'Jesus Christ Is A Hasidic And His Name Is',
    'The Revelation Of Christ',
    'Have Ness Name Is Bible Code',
    'Origin Of Equilibrium Coding',
    'The Voltage And The Frequency',
    'Spiritual Territories',
    'Ether Is A Shape In These Phrases',
    'The Mereologian Antichrist',
    'They Are Scared Of My Word O',
    'Jesus Is Coming Jesus Is Coming Hard Jesus Is',
    'EVERYONEEVERYONEEVERYONE',
    'You Already Know Who You Are',
    'Decode They Deserve Eternal Punishment For All The Suffering They Caused',
    'This Is A Sacred Text Please Interpret Correctly The Mathematics Of Words In The Matrix',
    'The Living Words Of God Emmanuel The',
    'The Ungrounded Of Sayings Only Emanuel The',
    'Angry Messiah Jesus Brings Sweet Oil Truth',
    'I Am The Rose Of Sharon And The Lily Of The Valleys',
    'Has Aec Friday May Fifth',
    'I Love You Alex Enrique Campain Vhodi',
    'Past Life In Nazareth As Jesus Christ',
    'True Birthdate Of Yeshua Christ',
    'True Birthdate Of Jesus Christ',
    'True Birthdate Of God',
    'King Of New Jerusalem',
    'I Am The Trumpet Angel',
    'God Above The All Of The All',
    'A Gift From The Creator',
    'Alex Campain May Fifth 1972 At 144',
    'How Much Is Alexandros Son Of Gematria? What Is The Meaning',
    'How Much Is God Above The All',
    'Elohim Tsebaoth',
    'Voice Of God',
    'How Much Is Voice Of God In Gematria?',
    'Yeshua Kyovu A Secret',
    'Sword Of Truth',
    'I Wield The Truth',
    'Bloodline Of The Gods',
    'Meet Divine Birth',
    'In Prophecy Of Isaiah',
    'The Antichrist Alex',
    'Game Of Selection',
    'Jesus Is Back Is Alive',
    'Divine Location Jesus',
    'Our Lord And Savior Alex Enrique Campain',
    'Our Lord And Savior Alex Enrique Palma Campain',
    'Our Lord And Savior Alex Campain',
    'Yeshua Christ The Word Of God Amor',
    'Holy Alex Son Enrique Campain',
    'My Son Alejandro Enrique Campain',
    'Yeshua Hides The Prophecy Of The Bride Of Christ',
    'The Laws Of God Shall Be Three Judge',
    'The Cia Hacked My Gematria Calculator',
    'Receiving The Decoded Messages',
    'How Much Is Receiving The Decoded',
    'The Son Of God Tells The Truth Back Off Amen',
    'Holy Spirit Does Not Desire Fame',
    'How Much Is My Name Is Zeus In Gematria?',
    'Who Is Called Christ',
    'We Are Hidden In Christ',
    'The True Source Of All Star Data',
    'Thousand Year Incarnation',
    'The Goddess Wife Of God',
    'I Am That I Am What I Am Will Be Legendary',
    'Their Will Never Be Heaven On Earth',
    'I Love Hawkeyes Numbers Love Me',
    'Resurrection Word Of The Kabala',
    'The Mark Of The Beast Is V',
    'Has G Jesus Birthdate',
    'Our Hopes Jesus Christ',
    'Old Hest Jesus Name',
    'I God Yeshua Calculated',
    'True Birth Year God',
    'The Noble Jesus',
    'Gematria Is Proof Of God And Other Gods',
    'Alex E Campain May Fifth 1972 At 144',
    'It Will Be Biblical',
    'Forty Days',
    'The Gates Of Heaven',
    'How Much Is The Gates Of Heaven In Gematria?',
    'See I Am The Messiah Alpha And Omega First And Last',
    'I Love You More Than Ever Before',
    'Install The Spirit Of Truth',
    'Transforming Earth Solutions',
    'Mrs Goddess And My God Godly Might',
    'Coherent Thought Sequence',
    'Decode Only A God Can Recognize A God',
    'Harmonics Of Sound And Color',
    'Decode Four Four Four',
    'Numbers Numbers Numbers',
    'The Merovingian Gematria Key',
    'I Secret Holy Bible Code',
    'Messenger Of God Ahasyab',
    'Has Being Of Prophecy',
    'Righteous In Christ',
    'Decode Are You Happy Now Yeshua',
    'We Prefer God Of Gods',
    'I Prefer God Of Gods',
    'Holy Gene Sophia Of The Trinity',
    'Telepathic Channeling Of Almighty God',
    'The C I As Being Afraid Of The Bride Of Yeshua',
    'Reincarnation Of The True God',
    'I Am A Being Of Light',
    'Above Him Open Up Back',
    'A Servant Of Lord God',
    'The Nazarene Essenes',
    'The Biblical God Is Satan',
    'I Am The Rider On The Storm',
    'Glory To G O D Alone',
    'God A Love Him',
    'Because He Is Alex E Campain',
    'Never Forgive Them',
    'What Is Your Name',
    'The New Testament',
    'Decode The Number Of A Man',
    'Jesus Reborn',
    'Because He Is Alex Enrique Campain',
    'The Arrival Of The Holy Spirit',
    'I Am The Man Of Faith And Holy Spirit',
    'The Simple English Gematria Is Real',
    'New Beginning Of Consciousness',
    'Survivor The Rebirth Is Over',
    'See The Messiah I Am The Chosen One',
    'Click Here For The Keys To My Mind',
    'I Send Satan And His Demons To Abyss',
    'Installed Two Pillars',
    'I Jesus Their Faithful',
    'Be Where Gods Residing',
    'The Resurrected Numerology',
    'Decode B Yeshua Keeper Of The Dragon',
    'Supreme King Of All Numbers',
    'Yeshua I Will Not Take The Job',
    'Frequency Four Four Five',
    'Theirs Real Love Right There',
    'I Always All Glory To Lord',
    'Your Mind Can Set You Free',
    'He Jesus Christ',
    'Jesus Is The Ark',
    'Nazareth Jesus A Woman Miracle',
    'Jesus Returns To Earth',
    'King And Lord Of New Jerusalem',
    'Decode The Creation Of Living Man',
    'Yahweh Reincarnated Last Year',
    'Gods Holy Grace And Mercy',
    'Words Of God Of Mary Magdalen',
    'Jesus Christo Nite For Eternity',
    'Holy And Divine Daughter Of Almighty God',
    'Jesus Christo Elite Chosen',
    'The Prophecies Of The Biblical Prophets',
    'You Are Not Like Them Find The Others',
    'Gods Birth Date Eight One Christ Death',
    'Our Savior Alexandro Enrique Campain',
    'He Who Is Judah King David Reborn',
    'Our Savior Alexandro E Campain',
    'K E J H G K E J H G K E J H G K E J H G K E J H G',
    'The Payroll Chamber',
    'Decode Yodi Never Walk Alone',
    'God And Son Vs Everyone',
    'The Fifth Element Is Nitro',
    'Decode Key To Escape The Matrix',
    'Decode The Love Of My Life Is Name',
    'Kings Of Kings And Lord Of Lords',
    'Apocalypse And New Son',
    'Hashem Is My Redeemer And Savior',
    'What Is Language Codes To Read Reality',
    'I Am Jehovah And There Is No One Else',
    'I Am Whose War',
    'I Love Jesus Christ',
    'Jesus Mary Mother Earth Grace',
    'Jesus The Strongest Affiliation',
    'Lord Goddess Jesus Lucifer Christ',
    'Hes Got The Whole World In His Hands',
    'Applied Mathematics Of Jesus Christ',
    'O I Chose You There Are No Coincidences',
    'Decode Mega Millions Winning Numbers',
    'Decode The Hidden Son The Veil Is Lifting',
    'The One Hundred And Forty Four Thousand',
    'Free Jesus Mary Rebirth Earth',
    'Jesus Messiah Cross The Key',
    'Jesus Servant Of S',
    'Our Lord And Savior Alexandro E Campain',
    'Our Lord And Savior Alexandro Campain',
    'The Way Kadosh Is Jesus Christ',
    'Yeshuvah Yishkel Yisrael Israel',
    'Holy Warrior Of Warriors Son',
    'A The Algorithm Of Consciousness',
    'The Consciousness Of Lamordiln',
    'Thou Shall Not Commit Adultery',
    'Jesus Is Lucifer In Disguise',
    'Catholic Jesus Is Lucifer In Disguise',
    'Decode Gematria Numbers Reveal Truth',
    'God Please Send Me Joyful Companions',
    'The One Whom Is On The Right Hand Of God',
    'The Holy Bride And Future Pet All Three',
    'The One Whom Is An Angel Of Lot Lamordiln',
    'Yeshua Is Risen For Me To Come Home',
    'Gematria Is Not Rubbish It Reads Codes',
    'Decode I Agreed To Fake Die In Order To Save God',
    'New Jerusalem Come',
    'What Is Absolute Truth',
    'Jesus Christ Is My Shepherd',
    'What Is Singularity',
    'Two Thousand Fifty',
    'The Seventh Dimension Of Consciousness',
    'Who Is Genetically And Mathematically Confirmed',
    'The Lord Yeshua King Of Kings And Lord Of Lords',
    'Isaiah Chapter Forty Verse Twenty Two',
    'Fuck You Jesus Yeshua Christ I Hate You',
    'Five Five Magnete',
    'Jesus Spirit Hours Physically',
    'One Language A Language For All Peoples Too Know',
    'Victory For Humanity Through Christ',
    'Install Matrix Code And The Book Of Revelation',
    'Our Lord And Savior Alexandro Enrique Campain',
    'Our Lord And Savior Enrique Palma Campain',
    'Youth Showing His Hand',
    'The Wrath Of Yahweh',
    'Jesus Christ Protected By The Order Of Christ',
    'Salvation And Glory And Power Belong To Our God',
    'Jesus Is Christ Yeshua Physics Facts',
    'Who Saved The World',
    'Codes Of The King And Eight Eight Are The Same',
    'Decode It Install Call On The Forces Of The Universe',
    'The Church Of Jesus Christ Of Latter Day Saints',
    'Jesus Christ The Reincarnation And Eternal Life',
    'Decode It Install Call On The Forces Of Life',
    'Decode The Jesus Christ In Your Savior',
    'The People Will All Be Free From The Matrix Soon',
    'Lucifer Yeshua Christ Are Brothers',
    'Decode Install The True Name Of The Most High God',
    'The Real Jesus Is V W In Heart',
    'Eight Thousand Eight Hundred Eighty',
    'The Sacred Geometry Of The Human Body',
    'See Jesus Is Wake Up',
    'Jesus Jesus n Perfect Code Of Code',
    'Everything Is Relevant',
    'Decode The Key Code Of Gematria Calculator',
    'Bride Of Christ Suffered Tragic Loss',
    'Holy Annointed One Of The Apocalypse',
    'Honor Your Father And Mother',
    'Our Lord And Savior Alex E Campain',
    'De Sacre Americus K G Jesus',
    'God He Declared From Morth',
    'Have New Name In Bible Code',
    'The Unsealing Of The Seven Seals',
    'Yeshua Is Coming Does Prepare',
    'Decode Do You Know Who You Are',
    'Always Trust Your Heart',
    'Be God Jesus Is Love',
    'Is A Little God Jesus',
    'Someone Who Has Returned From The Dead',
    'Selection Gematria Horseho Hestia',
    'You Will Know Him By His Tattoo',
    'The Almighty Gene Of The Holy Spirit',
    'I Asked And Received Help From Heavens Angels',
    'I Am The Twelve Surrounding Yes',
    'Morning Star The Negative Son Of God',
    'Yeshuas Let Your Will Be Done',
    'Our Savior Alexandro Enrique Palma Campain',
    'The Unique Name That Saves Humanity Is',
    'The Nature Of Jesus Christ In The Flesh',
    'Holy Is The Lord God Almighty',
    'The Cif Is K E J H G K E J H G K E J H G',
    'The Adversary Of The Devil',
    'The Fifth Wheel On The Wagon',
    'Get Lord And Savior Alexandro E Campain',
    'Da Messiah Is Of Sol Eko',
    'What If God Was One Of Us',
    'Jesus Sovereigns Of The Lord',
    'Surrender To The Good Lord',
    'The Lord Of The World Himself',
    'Divine Game The Angel Of The Holy',
    'The Messiah Chosen Yehoshua',
    'Jesus Was In The Military',
    'Jesus Hands Talk To You',
    'C Jesus Provides K',
    'New Born Alex Enrique Campain',
    'Seven Sevens Sevens',
    'Holy Grail Bloodline',
    'Forces On The Mission',
    'Birth Of Yeshua Christ Our Savior',
    'The Reincarnation Of Abaddon',
    'Jesus Christ In The Flesh Returns',
    'Alejandro E Campain May Fifth',
    'The God Of The Alphabet',
    'Alex Campain Birthdate',
    'Alex E Campain Birthdate',
    'Decode Gematria What Is The Point Correlation',
    'Alex Enrique Palma Campain Birthdate',
    'Decode Transition To Greatness',
    'Re Acting Like Jesus Act',
    'I Have Decided To Follow Jesus',
    'All Go The Blood Of G Jesus',
    'I Got Jesus Back For Her',
    'Friday Fifty Day Of The Year',
    'I Am Saying Yes To Jesus',
    'Way To Heaven',
    'Go Whale Your Secret God',
    'Bible Code Resonates Jesus Christ',
    'Who Is My Cosmic Soulmate',
    'Ivhoivhoivhoihv',
    'Then Shall The Righteous Answer Him',
    'The Lands Becomes The King Of New Jerusalem',
    'Christ Our Emmanuel Yehovah Yahweh',
    'Jesus Christ Has Two Births',
    'Return Of The King',
    'Jesus Arrival',
    'Decode Jesus Arrival',
    'Seeing The God Of The Old Testament M',
    'V Had The Father',
    'The Lores Book Of Ufo G Jr',
    'E Gods Code Testimonia Perfected Gene',
    'A Sleeping Prophet',
    'Jesus Reincarnate',
    'Decode The Holy Bible Code',
    'AEC Thinking No One So K',
    'Alex Campain Birthday',
    'The True Jesus',
    'Alex Enrique Campain Birthday',
    'Alex E Campain Birthday',
    'Mohammed Told The Truth',
    'Gematria History',
    'Jesus Miracle Heals',
    'Decrypting Languages',
    'Ten Holy Words',
    'The Only Number Is',
    'Earth Is For You',
    'Living God Gematria',
    'Removal Of The House Of Israel',
    'The Boy Who Became King',
    'Society Of Jesus',
    'Twin Flames Unite',
    'The Seventh Seal Is',
    'Happy Day',
    'My Father',
    'How Much Is My Father In Gematria?',
    'Hell I Has Birthright',
    'Book Of Life',
    'Knowledge',
    'Christ Is Risen',
    'Lucifer Christ',
    'Infinity',
    'AEC Birthday',
    'The Bloodline Is Of God',
    'How Much Is Aec Birthday In Gematria? What Is The Meaning',
    'Jesus Christ Is Back',
    'Tree Of Knowledge',
    'Christ Bloodline',
    'Aec Birth Certificate',
    'Our Savior Alexandro Campain',
    'Our Savior Alexander Campain',
    'Our Savior Alex C Campain',
    'God Yeshua Gematriology',
    'God Jesus Being Identified',
    'The Name Of God Jesus',
    'I The Name Of God Jesus',
    'The One Months Of Almighty God',
    'Its Time To End The Devils',
    'Hashem Star Of David',
    'Conclusive Proof Of God',
    'Faithful And True Witness',
    'As Be The Blood Of G Jesus',
    'Activate All Antichrists AE Antichrist All',
    'The Holy Spirit Loves You',
    'New Health Order',
    'Decode Judgment Is Coming',
    'I Jesus Hearts Angels',
    'The Bride Of Jerusalem',
    'I God Je Be Name Of Truth',
    'Confide In My Yeshua',
    'Give Christ Birth',
    'The Angel Of Destruction',
    'Christiansantichrist',
    'Childoftheholyspirit',
    'I Shall Destroy Lucifer',
    'Theres Two Bloodlines Of Christ',
    'I Am The Son Waiting To Understand',
    'Lucifer Incarnated In The Flesh Nimrod',
    'I Love You More Than You Know',
    'Seeing Jesus Christ Agony In The World',
    'Mankinds So Selfish Im Starting To Resent You All',
    'Divine Justice All God Jesus Christ',
    'C A Demon Does Not Be Having Authority K G Jesus',
    'Jesus Of Nazareth K G Sins Is Not A Sinner',
    'Resuscitation',
    'Jesus Resembles The Great I Am That I Am',
    'Pop Tech Is The Antichrist',
    'Divine Feminine',
    'How Much Is Divine Feminine In Gematria? What Is The Meaning Of',
    'Yehovah Is The Almighty Power Who Made All This',
    'Queen Of The Holy Trinity',
    'Lucifer Lost His Way K',
    'Jesus Is The God Damned Beast',
    'Everything Is I God',
    'Alex E Campain May Fifth Nineteen Seventy Two',
    'Seventy Nine',
    'Genesis Fifteen Prophecy',
    'Yahweh Satan',
    'Decode My Lord Delayeth His Coming',
    'The Devil Satan Is Power Less',
    'The Holy Father And Mother In Heaven',
    'God King Judgement Day',
    'Prophets Warnin',
    'Sons Of Light Prophecy',
    'Satan Sum Of Everything Equals To One',
    'Evil Never Prevails',
    'The Angel That Entertained Humanity Ss',
    'Nothing Can Stop Us',
    'Los Angeles Nuclear Bomb',
    'I Am The True Master Of Gematrix',
    'Oedipus Seventh King',
    'Jesus Is Caucasian',
    'Zeus Is Myth',
    'Cabal Has Paid Mark A King To Lie About Bride Of',
    'Cabal Paying For Sin K Jc',
    'Kingdomofgodiswithin',
    'Jesus Numbers',
    'C Jc Glory Be Proclaimed',
    'Eight Zero Eight Two',
    'Is A Gematria Divination',
    'Holy Rescue Of Sophia',
    'Nineteen Eighty Four',
    'How Much Is Un Antichrist Gov In Gematria? What Is The Meaning Of',
    'The Lawless Beast',
    'The Red Dragon Is The Sign Of The Rapture',
    'Three Six Seven',
    'The Key To Heaven',
    'Omnem Contraximus Condendis',
    'Resonating The Kingdom Of Heaven',
    'The Number Of God Is Eighty Eight',
    'See The Most Holy Angel Of Heaven',
    'Federal Bureau Of Investigation',
    'Nobody Can Stop What Is Coming',
    'Divine Conversation With God',
    'I Am Oedipus I Will Be Oedipus',
    'Vighneswara',
    'Surrounded In Stinking Evil',
    'Nine Thirty Two',
    'Mark A King Not Being Only Host For God To Use',
    'Activate The Prise Energy Grid For All',
    'God Is Heaven Please Forgive Me',
    'My Way To God',
    'Lord Do I Have Salvation',
    'Judge Of The Living And The Dead',
    'I Am Tired Of Seeing You Sin',
    'The Cabala Destroyed God Mak Mak',
    'Divine Twin Souls Of God',
    'Return A Curse To The Sender K God',
    'I Was Given The Holy Spirit As A Gift',
    'All Satanic Billionaires Are Erased Deleted Extinct M G',
    'Evil Is Finished Remove The Veil Of Illusion Now',
    'Mark A King Blasphemes The Holy Spirit Committing A',
    'The Grim Reaper',
    'Hebrew Gematria Calculator',
    'Allah Is The God Of The Heavens',
    'Calculate Jesus C',
    'Deliverance Belongs To Adonai',
    'Deliverance Messenger Of God',
    'The Final Place Of The Apocalypse',
    'Unconditional Love',
    'P O A C H I N G The Holy L A M B Of G O D',
    'The Holy Alphanumeric Code',
    'Heaven Sent Archangel Of Death',
    'Mark A King Is Avatar For God',
    'The Name Of The Antichrist',
    'The Heart Of The Righteous God Will Be Free',    'Turn To God Yehovah Y H W H World While You Still Have Time',
    'Jesus Is Simultaneously God The Soul Of God And The',
    'Jehovah Is Jove Jesus Is Zeus',
    'Stop Blaming God Jesus Christ Yeshua For All Your',
    'God Please Restore My Health And Abundance To What Is Intended',
    'Jesus Is Gathering Us Right Now To Fight The Final Battle',
    'Decode The Numbers Three Six And Nine Are Activated',
    'The Word Justice Can Be Made From The Lords Name',
    'A Man Of Goodness The Anointed One Return Of Jesus',
    'Decode Commanding The Galactic Program Of The Atlantic Elites',
    'Remember I Told You All Whos The Devil And You Said It',
    'The Most Powerful Triple Digit Number Eight Eight',
    'Decode The God Of This System Is On The Earth And He Hits',
    'Ah Well If The Islam Does Not Get The Alexandros',
    'Dear Lord Jesus Is My Spirit The Same Thing As My',
    'I Am The Descendant Of David Seventh Dec Mark Alan',
    'Make Your Path Straight With God',
    'There Two Bloodlines Of Christ',
    'Isis Is Goddess Of Eternal Life And Death',
    'Anu Heaven Yhwh',
    'I Am The End Times Anth Thar R God C',
    'What Happens If I Kill Myself',
    'How Much Is Anu Heaven Yhwh In Gematria? What Is The Meaning Of',
    'Mountain Of Youth Mirror Reflect',
    'The Innocent Will Inherit The Earth',
    'Lord God King David Pisces Aquarius',
    'Its The Jews',
    'God Very Tired',
    'C Be Bless For Mercy God',
    'God Is Giving',
    'Ten Eight Eighty Eight',
    'Im A Spirit Of Truth',
    'Holy Spirit Gold',
    'Nineteen Ninety Nine',
    'Eternal Day Of God',
    'C Glory Goes To I God',
    'Nineteen Zero Seven',
    'Presidential Election',
    'October Seventeenth',
    'Elon Musk Neuralink',
    'The Reptilian Archons',
    'My Numbers Say Im The Son Of Christ',
    'The Vortex Project',
    'Click Here To Find Yeshua',
    'Nuclear War This Year',
    'The Social Birth Of All',
    'I Am Not Of This World',
    'Direct Contact With God',
    'You Are The Way Finder',
    'Jesus Returned Q Am Back',
    'The Key Of Knowledge',
    'Jehovah Risen Prophecy',
    'Divine Game The Spirit Of The Holy Ghost',
    'I Think Mr Jesus Christ Has Risen',
    'O NEONEO NEONEO NEONEO NE',
    'The One In Seven Billion Who Knows The Truth',
    'The Illumination Of A Thousand Points Of Light',
    'A Man Will Return Who Understands And Perseveres',
    'The Sweet Message To Unlock The Door To Paradise',
    'Three Scoop',
    'Seven Three',
    'The One Jesus Sent Is',
    'In The Name Of David',
    'One Hundred Forty One',
    'In Love Inevitably',
    'Jesus Is The Heaven',
    'Quantum Physics',
    'Jesus Christ Indestructible',
    'Christ Square Day',
    'How Much Is Quantum Physics In Gematria?',
    'Yes Are The Son Of God',
    'Jesus Christo Total Punishment On The Beast',
    'Hour X Has Come The Secret Is The 13th Sense',
    'Jesus Christ Returning With Abba Yhvh And Now Of',
    'The Heaven Sacrifices Has To Stop Now Said Jesus',
    'I Am Recovering The Earth Not Destroying It O',
    'You Know Who I Am And You Know What I Need',
    'The Book Of The History Of Jesus Christ Son Of David Son Of Abraham',
    'He Can Restore Your Body And Your Soul',
    'Let The Doomsday Four Horseman Back Home',
    'I Am Pleased I Will Never Die',
    'Jehovah Roah The Lord Is My Shepherd',
    'Code Code Translation Perfected Gene',
    'I Am The Way And Truth And The Life',
    'Blessed Is He Who Comes In The Name of The Lord',
    'Jesus God Yeshua And Bride Of Christ Sharing A H',
    'Christ Return With A New House',
    'Jesus Christ God Son Savior',
    'Decode Sign Of Jesus',
    'Gracious Virtue Has Released',
    'Antichrist The Savior Of Man',
    'Shiva And Shakti Play And Cel',
    'Tempest Jesus Christ',
    'The Angel Of Jehovah Annihilated Lucifer Christ',
    'Jehn And I The Code Of God',
    'Where Are Lucifers Children',
    'True Star Morscy',
    'Savior Bring To Life',
    'Heaven Lord Of Lords',
    'The Story Of A Life On Planet Earth',
    'I God He Am Never Surrendering To A Cabel',
    'Ie The Hidden Son The Veil Is Lifting',
    'Satan Surrender To God Jesus K J',
    'I Surrender My Life To Jesus K A J',
    'Be The Second Coming Of Jesus Christ',
    'Mark King Code Of All Codes Matrix Cracked',
    'I Am Going To Saving Christianity',
    'The King Of Kings The Lord Of Lords Oh Yes He Has',
    'Jesus Is And Always Has Been The One And Only True',
    'Accept Yeshua As Messiah And Your King Yahweh',
    'Jesus Christ Has Returned And Cooking With Tv Talent Info',
    'His Handles Are You Can Look Um Up On You Creek Tube And',
    'King Jesus Queen Mary King Jesus Queen Mary King',
    'A A A A A A A A A A A A A A A A A A A A A A A A A A A',
    'I E S O U S K H R I S T O S K H R I S T O S L O R D J E S U S',
    'J E S U S Nos Z E U S',
    'J E S U S W As Z E U S',
    'I Have Become God',
    'Yehovah Elohim Spirit Of God',
    'Prophecy Of The Christ',
    'Gematria Has Returned',
    'Am I Am David I Am The Lion Of Judah I Am The King',
    'Annointed One Bleeding',
    'An Image Of God The Father',
    'God Be The Heir',
    'The Crucified GWH',
    'The Divine Angel Of Life',
    'The Great Holy One',
    'God Image Is Indestructible',
    'In King James Bible',
    'Roy Body Of Christ',
    'How Much Is In King James Bible In Gmatria?',
    'My Name Is Yesua',
    'Reluctant Messiah',
    'Q True Messiahs Of God',
    'Turin Shroud Of',
    'C Yeshua Saves Us',
    'Yeshua Saves Us',
    'Yahwehs Star Key',
    'Holy Spirit Flame',
    'The Saviors Heart',
    'The Lord Of The Earth',
    'The Yehweh Matrix',
    'Qc The Codes',
    'Qc I Am Light',
    'Eighth King The Lord',
    'How Much Is Qc The Codes In GMATRIA?',
    'I AM STRENGTH',
    'God The Alpha The Omega',
    'I AM SO Lonesome',
    'Amun Ra God Of Gods',
    'Nothing Shall Be Hidden',
    'Ye Are Gods',
    'I Am Thee Architect',
    'I Am Thoth I Am Abrahadsim',
    'Havin God D N A',
    'I Am The Plan',
    'Dna Decided The King Of Kings',
    'A Proof Gods A Man',
    'Gods Breath',
    'He Died For All',
    'Because Hes God',
    'Perfect Divinity C',
    'Archangel Mary Magdalene',
    'The Way Of Yehovah',
    'Goodbye To The Beast',
    'Yhwh Is Forgiven',
    'The Angel Of Disaster',
    'Jesus Is God And King',
    'Yahweh Is A Fallen Angel',
    'Jesus Is Our Sin',
    'King Of Heaven And Earth',
    'Jesusmisviador',
    'The Spirit Of Hayah',
    'The Blood Of My Blood',
    'The End Of Your Life',
    'Presence Of The Lord',
    'God The Holy Ghost',
    'Three Six Eight',
    'The Order Of Jesus',
    'The Redeemer The Lord',
    'The Greatness Of God',
    'Allah Divine Phoenix',
    'Ihvh Ihvh Is Elohim',
    'Jesus A Twin Of God',
    'I Am Yeshua Soul',
    'A New Jerusalem King',
    'Clense The Earth',
    'Holy Graal',
    'Creator Gods',
    'A Son Of Great I Am',
    'The E N D Program',
    'Face True God Dad',
    'The Elites Hidden Agenda',
    'THE G R E A T Escape',
    'The King Of All Earth',
    'Name Him King Ra Of Light',
    'I Am The Eternal King',
    'Gematria Made For G O D',
    'Jesus Frequency',
    'The True Holy Land',
    'I Holy Spirit Child',
    'You Choose Christ',
    'Virgin Of Guadalupe',
    'Jesus I Am Back Jesus',
    'Behold He Jesus Comes',
    'He Saves Everyone',
    'He Is Revelation God',
    'Facing Lucifer And Satan',
    'Aaron Universe God',
    'Messiah Of Nihilism',
    'Declare The Word Of God',
    'Called Jesus Christ',
    'Three Trumpets',
    'Our Cosmic Origin',
    'Christ And Cross Head',
    'C The Messiah Crucified',
    'The Created God Of Earth',
    'Joshua Is My Son',
    'The Prophets',
    'Yahweh And Azathoth',
    'The Lords Birthdate',
    'The Days Of The Antichrist Birthmark',
    'Lion And The Lamb',
    'Lucifer Is The Antichrist',
    'Lord God Consciousness',
    'Hector Omar Reyes',
    'Jesus Christ Dies',
    'How Much Is King From Heaven In Gematria? What Is The Meaning Of',
    'Yodhehvahyeh',
    'Yeshua Looks Like',
    'Everything Is Code',
    'Christ Divine Blood',
    'Gods Messenger Ss',
    'The Luciferian Birth',
    'Is My Son Jesus',
    'Israeli King Jesus',
    'Calculate GMATRIA',
    'Jesus In The Bible Is',
    'Isaiah Thirteen Nine',
    'A Manifestation King',
    'A Face Of Jesus Christ',
    'King Davids Bloodline',
    'The Face Of A Christ',
    'Secret Of God Decoded',
    'Jesuss God Jehovah',
    'Ancient Giant Zeus',
    'A The Divine Phoenix',
    'Hollierith Census',
    'Aquarius Venus',
    'Invicto Puerom',
    'I Am Who I Am And I Am Love',
    'Gods Ultimate Gift',
    'Decode I Am The Architect Of A Matrix',
    'You Are Divinely Protected',
    'Decode The Seven Spirits Of God',
    'Ripple Through The Matrix',
    'Acting As An Agent For A Higher',
    'We Are Divinely Protected',
    'The Host Of The Living Gods',
    'Annointed True Prophet Of God',
    'Is One Of The Ten Horns Of Revelation',
    'Install Jesus Christ Of Nazareth Eve',
    'The Highest Yahweh',
    'Jesus And Mary Magdeline',
    'I Am Christ The Doom Of All Things',
    'Jesus Is Comming',
    'Elohims Knowledge',
    'Jesus Christ The Teacher',
    'Demonic Abrogation',
    'The Second Coming Of Jesus',
    'Jesus My Gematria M K',
    'I Am Going To Destroy Christianity',
    'The Current Soul Of Jesus Christ',
    'Allah Allah Allah Allah Allah Allah Allah Allah',
    'Become A Dasher',
    'Names Of God',
    'End Of Satan',
    'You And Me Are One',
    'Lions Of Israel',
    'End Of The Illusion',
    'The Lion Of Judah David',
    'Jesus Is Real',
    'Shekinah',
    'Starlight Ray Of God',
    'True Love Awakens The Christ Within',
    'Unlock Unmapped And Undivided Abilities',
    'Hey Shin Yod Kaf The God Of',
    'Zeus Reincarnation',
    'Delete The Vatican Alex',
    'The King Of New Jerusalem',
    'Gospel Of Matthew',
    'Jesus Died On A Cross',
    'Jesus The Evenjel Of Reincarnation',
    'Matrix Code And The Book Of Revelation',
    'Yod Hey Shin Yod Kaf The God Of Heaven',
    'All Glory Belongs To Jehovah The Father',
    'Jesus The Miracle Of Peace',
    'Gods Chosen One For Me Is Named',
    'Sits On The Right Hand Of God',
    'The Savior Breaking The Code',
    'Unveil Truth God',
    'Chosen By The Holy Ghost',
    'How Much Is Chosen By The Holy',
    'The Greatest Challenge Of David Nathaniel Bridge',
    'Heaven Heaven Heaven Heaven Heaven Heaven Heaven',
    'Heaven Way To Heaven Heaven Heaven',
    'The Angel That Entertained Heavenly Go',
    'The Rarest Human Of All King D',
    'Life Happens Thru You And Not To You C',
    'Gematria Is Proof Of God And Other Beings',
    'The Bible Jesus',
    'Jesus Loves You',
    'How Much Is Jesus Loves You In Gematria? What Is The Meaning Of',
    'How Much Is The Holy Trinity In Gematria?',
    'How Much Is Prophets Of Yahweh In Gematria?',
    'God Rules The World With Truth And Grace',
    'Decode The Sweet Human On All King David Reborn',
    'Gods Grace Shall Restore Harmony',
    'House Of God',
    'Decode Mary Magdalene And Jesus Christ',
    'She Makes Love To The King Of Kings',
    'Permanent',
    'Selective Return',
    'The Unknowable God',
    'Morningstar Jesus Christo',
    'Holy Gods Infinite Power',
    'Edge Of The Living And The',
    'Divine Prophet Of God',
    'God The Creator Of The Golden Rules',
    'The Tenth Commandment',
    'Rising From The Ashes',
    'Judgment Day Is Coming',
    'Rapture',
    'Most High',
    'Firmament',
    'How Much Is Alexandros Son Of God',
    'How Much Is It Will Be Biblical In Gematria? What Is The Meaning Of',
    'God Is The Greatest Script Writer Of All',
    'Life Happens Thru You And Not To You',
    'Acting As An Agent For A Higher Order',
    'Devastator',
    'Date Of Light Prophecy',
    'Divine Communication',
    'A Vessel A Vessel Of Christ',
    'Vessel A Vessel Of Christ',
    'Jesus H Christ',
    'Protected By God',
    'The True Purpose Of Triple Eight',
    'I Am Your Retribution',
    'How Much Is I Am Your Retribution In Gematria?',
    'Superhuman Frequency',
    'Seventh Trumpet',
    'How Much Is The Bible Jesus In Gematria? What Is The Meaning Of',
    'How Much Is Devastator In Gematria? What Is The Meaning Of',
    'Trial Is Proof Of God And Other',
    'C Heavens Be So Close K God',
    'Who Is King David',
    'Prayers Answered',
    'King Not Being Only Host For God',
    'Decode Jesus The Nazarene',
    'Yehoshua Is Yeshua',
    'Billion Will Be Alive',
    'The Only One The Lord',
    'Gematric Encryption',
    'The Order Of Melchizedek',
    'Yahshua Is Hayley',
    'Thee Lord Savior Alex Enrique Campain',
    'The Great White Throne Is The Midst Of The Earth',
    'There Is No Religion Or Law Higher Than Truth',
    'Gods Plan Of Salvation Is The Ten Commandments',
    'Jesus The Carpenter Of Earth Died For Our Sins',
    'Thee Lord Savior Alex Enrique Palma Campain',
    'The Veil Is Lifted For All To See The Truth',
    'Yeshua Christos Theos Soter',
    'Christ The Redeemer Becomes King David Manifest',
    'Alejandro Palma Campain',
    'Numero De Dios',
    'Gates Of Hell Is Open',
    'ONEFOURFOURONE',
    'Israels Saviour',
    'Two Aspects Of God',
    'Create Heaven On Earth',
    'Christ Dead In Cross',
    'I A Deathly Afraid Of I God',
    'CIA Death Penalty Afraid Of God Jr',
    'Jesus Arrival Save The Children',
    'Am A Vibrational Match To Sour',
    'I M The Way The Truth And The',
    'Surrender To Jesus Christ',
    'Lighty Gods Denmat',
    'Communion With Source',
    'Yodhehvavheh',
    'Andro Enrique Campain',
    'God Called The Firmament Heaven',
    'Cosmic Reset In Progress',
    'The Name Dna And Soul Of Chris',
    'Jesuschristconscious',
    'Jesus Is Our Salvation',
    'Thejesuschristmatrix',
    'Andro Enrique Palma Cam',
    'What If God Was One Of',
    'Yeshua Christ Is The Real Name Not Lucifer',
    'Almighty Gods Decreed Judgment',
    'Conversation With Source',
    'Yodheyavah',
    'How Much Is Yod Heh Vav Heh In Gematria?',
    'The Work Of The Holy Spirit',
    'He Really Is Jesus Christ Visit',
    'The Righteous Melchizedek',
    'I Am A Vibrational Match To Source',
    'I M The Way The Truth And The Life',
    'Jesus Seminar',
    'Thephonedrome',
    'Lord Shiva Exist',
    'The True God Q Code',
    'I Am That I Am I Am I Am I Am',
    'You Are My Everything',
    'Zero Zero Zero',
    'O Adonim Are Yeshua And Mary',
    'I A M Death A Deadly Blow To The Cabel',
    'Presidential Immunity',
    'Superior Bloodline Of God',
    'January Twenty Third',
    'Judgements Come For Cabala',
    'Judgement',
    'Jesus Raised From Dead',
    'The True God Love Q Code',
    'The Name Seo And Soul Of Christ',
    'Jesusofnazareth',
    'Crucifixion Of Jesus Christ',
    'The Holy Bride Of Jesus Christ',
    'Yeshua Yeshua Christ',
    'Yeshua Yeshua Christo',
    'Thee Lord Your Savior Alex Campain',
    'You Are The Reincarnation Of Lucifer',
    'Yeshua Saves The World',
    'Yeshua Goding With Fire And Vengeance',
    'Ahasis Has A New Identity',
    'The E Of God Are The Foundations Of All Mighty God',
    'The E To Reveals Itself ToAn Open Mind The Lord',
    'The Sea Of God Is Amongst Us The Light Is Here',
    'The Most Powerful People In The World',
    'The Power Of The Word',
    'The Final Code To Break Sorcery Second Coming Two',
    'He Who Created The Universe',
    'Thee Lord Our Savior Alex Enrique Campain',
    'Thee Lord Our Savior Alex E Campain',
    'John The Baptist Crown Of Yeshua',
    'A Refreshing Experience To Remember',
    'The Quantum G R Experiment',
    'The Second Time He Came Back With Power',
    'Hollywood',
    'Jesus Is Our Ace Up Our Sleeve',
    'Finding Your A E',
    'Thee Lord Our Savior Alex Campain',
    'Alexander Four Four Four Four',
    'Find The Source Of A E Life The Event',
    'Vimana Ordo Seclorum',
    'Truth Will Not Be Silenced',
    'You Are Divine Twin Flames',
    'Victoria Palma Campain',
    'Jesus An Astronomical Silence',
    'Reveal Secret Holy Bible Code',
    'God Prophet Online Message For God',
    'Thee Lord Savior Alex E Campain',
    'Divine Translations Of Gematria',
    'The Dewy Of Jesus',
    'Son Of Yehovah The Son Of Yeshua As Father',
    'Annointed Holy Spirit Within Them',
    'The Theory Of Complex Simplicity',
    'The King And Savior Lord Aec',
    'The King And Savior Aec',
    'Our King And Savior Aec On The',
    'Our God And K Savior Aec On The',
    'Our G Lord Savior Aec On The',
    'Christ Alex Campain At',
    'The Christ Alex Campain',
    'Hebrew English Gematria',
    'Fire Is The Magic Number',
    'The Meaning Of Harders',
    'C Our Christ Alex Campain',
    'Christ Alex E Campain',
    'Savior Alex Enrique Campain',
    'The Re Incarnation Of Yeshua Christ',
    'Savior Aec Mount Of Olives',
    'Jerusalem Stone',
    'How Much Is Jerusalem Stone In Gematria?',
    'Vhodi',
    'The Holy Birth Of Alex Campain',
    'Fountain Of Youth',
    'Rape The Lord',
    'Number Language Of Light',
    'Take Back Your Power',
    'Jesus Life Is Sacrificial K',
    'Official Heir Of Jesus',
    'God Jesus Identified K',
    'Revealed Is New Name Of',
    'Decode Youll Never Walk Alone',
    'God And His See Vs Everyone',
    'Future Will Prove Past',
    'Decode The Love Of My Life Is Nameed',
    'King Of Kings And Lord Of Lands',
    'The Absolute Truth',
    'Most Holy Wife Of Jesus Christ',
    'Sword Of The King',
    'White Rose',
    'Something Special Coming Soon',
    'Transcription Of The Soul',
    'Home Of Creator Is Book Of Genesis',
    'You Are A Ethical Miracle Unfolding',
    'You Are A Free Man',
    'Holy Spirit Thou Born In Me',
    'Sex Is So Vile Who Think I Am',
    'The Eternal Deity Of Heaven',
    'Holy One Of Israel In The Midst Of Thee',
    'I Put A Lot Of Messages For You Here',
    'Jesus Christ Root By Jehovah',
    'The Parents Of The Holy Spirit Itself',
    'The Key To Unlocking Your Divine Path',
    'Excites Twenty Five Twenty Two',
    'I Am The Human Host Of Jesus Of Nazareth',
    'Jesus Christo Returns As The Lion',
    'Holy Spirit Is Gnostics Apocalypses',
    'Thank You Jesus Thank You Lucifer',
    'Isaiah Chapter Forty Nine Ninth Verse',
    'Jehovah Is My Strength And Salvation',
    'Chosen Pleiadeans Of The Lord God Almighty',
    'The Transdimensional Cube Of Metatron',
    'Jesus Is The Eye Of The Storm',
    'Spirit',
    'Y H V H',
    'Clear Alex Enrique Campain',
    'How Much Is Y H V H In Gematria? What Is The Meaning Of',
    'Rapture Of The Bride Of Jesus Christ',
    'Thee Lord And Savior Alex E Campain',
    'Jesus The Carpenter Of Earth',
    'Jesus Has Received Begin Joy',
    'Tree Of Knowledge Of Good And Evil',
    'I The Lord Thy God Are A Jealous God',
    'Thee Lord And Savior Alex Campain',
    'Sacrificed On A Stake Two Nails',
    'Cheryl Ann Yeshua Campain',
    'Messianic Jewish Alliance Of Earth',
    'How Much Is Christ Alex Enrique',
    'Saving Humanity Jr',
    'I Jesus Christ Am The One True Gangster',
    'Spring Is Here Jr',
    'There Are No Coincidences True Prophet Of God',
    'Jehovah Never Fail',
    'Thou Shall Do Whatsoever Thou Worts',
    'There Are Nine Gods All Together',
    'Holy Goddess To The Lord Your God I Am',
    'Jesus Und Ich Sind Gttlich Verbunden',
    'Bendito Is Religion Destroyed',
    'King Of Jesus',
    'How Much Is King Of Jesus In Gematria?',
    'Holy Feminine Side Of The Divine',
    'A Savior Lord Alex Campain',
    'What Is The Fifth Element',
    'I Am Of God Who Art In Heaven',
    'Intelligent Infinity',
    'AEC At Mount Of Olives I',
    'AEC On Mount Of Olives I',
    'By The People For The People',
    'Yeshua Ordo Seclorum',
    'You Back From The Dead Number',
    'God The Devil God',
    'Holy Avenger',
    'Remembers True Birthday',
    'A Foundation Of Heaven',
    'Jesus Christ Has Your Money To Me A Sinner',
    'Knights Templar',
    'Allah Akbar',
    'Judgements Comin For Cabal',
    'Cabal Is Going Crazy K God Je',
    'Christ Is The Real Name Not',
    'The Wrath Of The Holy Spirit',
    'The Angel Of Death The Mark Of The Beast',
    'Truly This Is The Son Of God Alex Enrique Campain May',
    'King Of Kings And Lord Of Lo',
    'The Almighty Sophia',
    'Hes A Chubby Chaser',
    'The God Gene',
    'A Satan And Lucifer Chained Together In Hell',
    'Satan Fleeing From Me Je',
    'Man Of God',
    'Demolish The Devil God',
    'How Much Is Decode In Gematria?',
    'Decode Eternal Hell Exist',
    'The Mark Of The Beast Scenario',
    'Saint Michael The Archangel',
    'Nine Nine',
    'Double Cross',
    'Three Three Three',
    'The God Of Islam Tell On Yourself',
    'Demonic',
    'Raised Jesus From Dead',
    'Diabolos',
    'Mark A King',
    'Arrived',
    'Seven Threes',
    'Alejandro Enrique Campain Palma',
    'Dark Knight',
    'How Much Is Black Horse In Gematria?',
    'What Is God So Afraid Of',
    'Arrival Of A Deity',
    'Return Of The Jedi Knight',
    'He Ended Poverty',
    'Only God Can Judge Me',
    'The Name Of The Divine Mate Of Michael Angel',
    'Mandela Effect',
    'Shift Out Of False Reality',
    'He Married God Jesus',
    'Warrior Lord',
    'Lord Have Mercy',
    'No One Be Able To Curse Me Je',
    'God Hidden Bible Code',
    'Code Of The Torah',
    'Alpha Omega M',
    'Alex E Campain',
    'Elohim Spirit',
    'Extraterrestrial Qliphoth',
    'King Saviour Alex Enrique Palma Campain May Five Nineteen Seventy Two At One Forty AM',
    'Savior Alex Enrique Palma Campain May Fifth Nineteen Seventy Two At One Forty AM',
    'Christ Adonai Lord Alejandro Enrique Campain Friday May Five Nineteen Seventy Two at One Forty AM',
    'Our Saviour Lord And Christ Alex Enrique Campain Friday May Fifth Nineteen Seventy Two One Forty AM',
    'AEC Alex Enrique Campain Eighty Eight Seven Seventy Two To Anyone',
    'El Alex E Campain born May Fifth Nineteen Seventy Two At One Forty AM',
    'God Elohim Alex Enrique Campain May Fifth Nineteen Seventy Two At One Forty AM',
    'YHWH God Alejandro Enrique Palma Campain May Fifth Nineteen Seventy Two At One Forty AM',
    'El Elyon Alejandro E Campain May Five Nineteen Seventy Two At One Forty AM',
    'Elohim Alex E Campain May Fifth Nineteen Seventy Two At One Forty AM',
    'El Shaddai Alex Enrique Palma Campain May Fifth Nineteen Seventy Two At One Forty AM',
    'Adonai Alex E Campain May Fifth Nineteen Seventy Two At One Forty AM',
    'Rapha Alejandro Enrique Palma Campain May Fifth Nineteen Seventy Two',
    'Rafa Alex Enrique Palma Campain May Fifth Nineteen Seventy Two At One Forty AM',
    'Messiah Alex Enrique Campain May Fifth Nineteen Seventy Two At one forty AM',
    'Moshiach Alex E Palma Campain May Fifth Nineteen Seventy Two',
    'El Mesías Alejandro P E Campain May Fifth Nineteen',
    'Mashiach Alejandro Enrique Palma Campain May Fifth Nineteen',
    'King Alejandra P Palma Campain May Fifth Nineteen',
    'Lord Alex Enrique Campain May Five Nineteen Seventy Two One Forty AM',
    'The Moshiach AEC Alex E Campain May Fifth Nineteen Seventy Two',
    'El Elyon Alex Enrique Campain May',
    'El Shaddai Alex Enrique Campain May Fifth Nineteen Seventy One Aec Born',
    'Rapha Jireh Alex Enrique Palma Campain May Fifth Nineteen Seventy Two',
    'Moshiach Alex Enrique Palma Campain May Five Nineteen',
    'Lord Alex Enrique Palma Campain May five One Hundred Ninety Seven',
    'King Alex Enrique Campain May Fifth Nineteen Seventy Two At One Forty AM',
    'Savior Alejandro Enrique Palma Campain May fifth',
    'El Elyon Alejandro Enrique Campain May Five Nineteen Seventy Two One Forty A.M',
    'Elohim Alex E Campain Friday May Fifth Nineteen Seventy Two',
    'El Shaddai Saviour Alex Enrique Campain Born Friday May Fifth Nineteen Seventy Two At One Forty AM',
    'Our King Christ Alex Enrique Campain Born Friday May Fifth Nineteen Seventy Two At One Forty AM',
    'Lord Alex E Campain May Fifth Nineteen Seventy Two At One Forty AM',
    'Christ Alex Enrique Campain May Fifth Nineteen Seventy Two At One Forty A.M',
    'God Alejandro Enrique Palma Campain May Five Nineteen Seventy Two At One Forty A.M',
    'El Elyon Alex E Campain May Fifth Nineteen Seventy Two',
    'Elohim Alejandro Enrique Palma Campain May Fifth Nineteen Seventy Two At One Forty AM',
    'El Shaddai Alejandro Enrique Palma Campain May Five Nineteen Seventy Two',
    'Adonai Alex Enrique Palma Campain May',
    'He is Our King Christ Alejandro Enrique Campain May Fifth Nineteen Seventy Two One Forty AM',
    'Messiah Alex Enrique Campain May Five Nineteen Seventy Two One Forty AM',
    'YHWH Alex Enrique Campain May Fifth Nineteen Seventy Two',
    'Alex Enrique Palma Campain YHWH The King Of Heaven',
    'The Illuminati Antichrist',
    'The Righteous One',
    'My Eternal Name',
    'Discover Who You Are',
    'Alex Campain In Jesus Christ Of Nazareth',
    'My People Who Are Called By My Name',
    'Maria Orsic Daughter Of Odin Alex Tree',
    'Alex Campain Is Jesus Christ Of Nazareth',
    'Happy Birthday May Fifth Alex Campain',
    'Thee Lord And Savior Alex Enrique Campain',
    'Six Hundred And Sixty Six',
    'K Is Yeshua Christ Lucifer Twin B',
    'Happy Birthday May Alex Enrique Campain',
    'May Five Alex Enrique Palma Campain',
    'Happy Birthday May Alex Jha',
    'Yahweh Resealed',
    'May Fifth Alex Enrique Palma Campain',
    'God Jesus Reborn',
    'The Gospel Truth Of Mary Magdalene',
    'The Universe Loves Humanity',
    'Chosen By God Yeshua',
    'Johny The Only Begotten Son',
    'Spirit Of Grace',
    'Godly',
    'How Much Is Clear Alex Enrique Campain',
    'Is Jesus Messaging',
    'Y All Message Imports Ororo Earth',
    'Human Gestation Period',
    'How Much Is Yahovah In Gematria?',
    'Yahovah',
    'He Is Of Holy Eternity',
    'The Purpose Of Gematria',
    'Five Loaves The Eagle Has Landed',
    'Jesus Paid Our Ransom',
    'Money Luck Love',
    'Jesuschristconcious',
    'Theory Of Relativity',
    'The Voice Of Elohim',
    'The Great Awakening',
    'The Bride Of Christ',
    'Prophet Manifest K',
    'God Je Showin Who I Am',
    'Decode Who Is Daddy Jesus Messiah',
    'Holy Spirit Told Me Everything Gonna Be Aright',
    'Messiah Lives In United States F B I',
    'Decode Y He Holy Dead Of Almighty God',
    'Five Times Faster Radio Frequency',
    'The Return Of The Superhumans',
    'Mother And Successor Of The Universe',
    'The Great Architect Of The Universe',
    'The Divine Child Is The Chosen One Of God',
    'Yeshua I Have No One To Love Me',
    'Black Messiah',
    'Gods Choice Iam',
    'Beastman',
    'The One',
    'He Know The Truth',
    'Kingdom Has Come Not Youre Harl',
    'He Returned To Help Man',
    'Alpha And Omega The Beginning And The End And The First And The Last M Q',
    'Beast Beast Beast Beast Beast',
    'The Gospel Of Jesus',
    'Return As A Lion',
    'Alex Enrique Palma Came',
    'Alejandro Enrique Campain pal',
    'The E To Reveals Itself To An Open Mind The Lord',
    'Thee Lord Savior Alex Campain',
    'Revival Secret Holy Bible Code',
    'The Witness Of The Holy Father',
    'Ys Business Jesus Messiah',
    'A C This Our Earth Our Universe',
    'Yeshua Water',
    'Daughter Of The Holy Trinity',
    'Provided His Evidence',
    'He Who Is The Lancastetian King',
    'A Christ Is Here And No One Believes',
    'I Am That I Am God God God God God God',
    'An Age Of Aquarius Holy Birthday',
    'The Secret Of Eternal Life Resended',
    'Confucius Jesus Christ',
    'H Yeshua Y H W H Christ',
    'Daughter Of The Holy Trinity',
    'The Kingdom Of Yehovah Jehovah',
    'To All Humanity Alex Enrique Palma Campain Is',
    'Messiah Jesus Gematria',
    'I Am The God Of Thy Father The God Of Abraham The',
    'Rebirth Should Be Sacred Not Corrupted And',
    'To All Humanity Alex Enrique Campain Is Jesus Christ',
    'Yes Know He Would Be Sacrificed',
    'Jesus Was Already Crucified For Us',
    'Yes Know Who You Are',
    'The Vatican And The City Of Rome Are Going To Get',
    'Your Faith In God Has Become Known Everywhere',
    'Chosen And Created By God Elohim Yhwh',
    'Youtube Loves You Trust Me',
    'JESUSCHRISTJESUSCHRISTJESUCH',
    'Jesus Christ Of The Four Winds',
    'The Announcement That Was Will Be',
    'You Are My Saviors And I Am Forever Grateful',
    'I Am The Son Jesus Of Nazareth Living Son Of God',
    'I Am The Son Jesus Of Nazareth Living See Of God',
    'A Prophecy Of The Two Witnesses',
    'Alex Campain Was Trained From Birth To Do This',
    'Lucifer Jesus Yeshua Oholei',
    'Are You Willing To Fight For Me That Is The Question',
    'Reincarnation Of The True Jesus Christ God Dna',
    'I Am The Root And The Vine The Promised One Jesus',
    'May The Holy Ghost Be With You',
    'Decode It Restore The Blood Of Jesus Christ Of Nazareth',
    'Wrath Of God Revealed From Heaven',
    'I Am Not Getting Paid For This I Just Do It Because I',
    'Reveal The Story Of Life On Planet Earth From',
    'I Am Alpha And Omega The First And The Last',
    'The Word Of God Shall Live Forever',
    'Decode Gmatria What Is The Point Correlation',
    'I Am The Coming Of The Lord God Almighty',
    'The One Who Knows The Real Truth',
    'Who Is Mani Left Salvation And Holy',
    'Jesus Was Married To Mary Magdalene',
    'Not Worth Saving Humanity',
    'Decode God So Loved The World That He Gave His Only Begotten Son',
    'The Most Important Event In The History Of Humanity',
    'I Am Not Going To Let You Go Q',
    'Genesis One In The Beginning God Created The',
    'The Two Witness Of The Father',
    'Jesus Messiah All The Way Home',
    'Alex Enrique Campain The Second Coming Of Jesus Christ',
    'He Also Reigns Over The Earth',
    'Spirit Manifest In Forms Of The Universe',
    'Because I Love You My Dear Children',
    'Numerical Synchronicity At The End Of Time',
    'Thank You God Thank You God Thank You God',
    'Aec May Fifth Second Coming Of Jesus Christ',
    'How Can I Trust You',
    'What Is The Gematria Calculator',
    'Jesus Is The Owelry',
    'Jesus Is The Word',
    'Jesus Of Nazareth Is God In The Flesh',
    'Jesus In Gematria Is The Flesh',
    'Christ Is Not What Any Of You Think',
    'He Who Sowed The Good Seed Is The Son Of Man',
    'There You Go Get Your Acknowledgement',
    'God Is A Human On Earth Birth Birthday Code M C H S',
    'K A D O S H',
    'Mother Earth Is Under Ant Of Stress',
    'God Jewish Power',
    'Jesus Walking Human',
    'How Much Is Jesus Walking Human',
    'Alex Campain The Second Coming Of Christ',
    'Alex E Campain Second Coming Of Christ',
    'Alex Campain Second Coming Of Christ',
    'For All Humanity Alex E Campain Reincarnated Into',
    'Holy Wisdom Bride Of Almighty Jesus',
    'For All Humanity Alex Campain Reincarnated Into Jesus Christ',
    'Saved By Yeshua In Yahweh',
    'The Most Important Thing You Can Give Her Is Your',
    'Jesus Said Whatever You Ask In My Name I Will Do It Because I Am The Son',
    'Your Reason To Live Is To Defend Your Lord In Blood',
    'Is The Glory Of God To Conceal A Thing But The',
    'There Are Underground Child Meat Markets In The',
    'Y H W H Y H W H Y H W H Y H W H Y H W H',
    'I Love Everyone Unconditionally But Respond To Kindness',
    'You Yes Devils Scared Of Me Stop Censoring Me',
    'Am Second Coming Of Jesus Christ',
    'The Holy Spirit Is With Him',
    'The Lord Gave All That He Made To Us',
    'Jesus Christ Son Of The Lord',
    'AEC Second Coming',
    'How Much Is The Son Of Man In Gematria? What Is The Meaning Of',
    'I Am The Sovereign Prince I Have The S 500 Of God',
    'Alex E Campain Is The Second Coming Of Jesus Christ',
    'Decode The Sword Of Jesus',
    'Law Of Yehovah',
'SAVETHECHILDRENSAVETHECHILDRENSAVETHECHILDREN',
    'Law Of Yehovah',
    'Jesus English Gematria',
    'The Truth Will Always Endure',
    'You Are All Going To Get What You Deserve',
    'Hebrews Code English Into Hebrew Using The Gematria Calculator',
    'Ignoring The Wicked Only Increases Their Power On Earth',
    'John Has Everything We Need',
    'To All Humanity Alex Enrique Palma Campain',
    'Kjv Bible Rewritten By European Monarchs',
    'Yeshua I Want To Connect With You',
    'The Cia Uses Direct Energy Weapons To Attack Your',
    'The Universal Law Of The Universal Creator',
    'JESUSCHRISTJESUSCHRISTJESUSCH',
    'Explain The Formula For Kingdom Of Heaven And Earth',
    'I Am Finally Completely Connected To Jesus Christ',
    'Abba YHWH Abba YHWH Abba YHWH Abba YHWH Abba YHWH Abba YHWH',
    'Abba Yah Abba Yah Abba Yah Abba Yah Abba Yah Abba',
    'Aleph Bet Gimel Dalet Hey Vav Zayn Chet',
    'Matthew Chapter Twenty Four',
    'God Is Frequency Energy And Vibration',
    'To All Humanity Alex Campain In Yeshua Christ',
    'Those Who Are With Him Are Called Chosen And',
    'He Has Opened The Bible And Interpreted It Accurately',
    'To All Humanity Alex E Campain In Yeshua Christ',
    'Conspiracy Theories Are The Search For Truth',
    'Holy Is Now And Holy Is Then',
    'Joy Of My Salvation',
    'To All Humanity Alex Enrique Campain In Yeshua',
    'Vhodi Myah',
    'Smile Jesus Loves You',
    'I Love You Jesus Me Too',
    'How Much Is Smile Jesus Loves You',
    'Jehovah Is The God I Know',
    'The Hidden Gematria Code Of God Is All Gods Birth',
    'God All Mighty Please Bring Balance And Judgement',
    'Yod Hey Vav Girial Hydrogen Nitrogen Oxygen Carbon',
    'Thank Yeshua I Heard What You Are Doing For Me So',
    'Alex E Campain The Second Coming Of Jesus Christ',
    'Christmas Is Not December Twenty Fifth But The Day Our Mother Lord Gave Good fruit Heal',
    'I Can Do All Things Thru A Christ Whose Soul Lives In Me The Son Of God',
    'The Holy Grail Is The Seed Of Yeshua Christ Reborn',
    'To All Humanity Alex E Campain Reincarnated Into',
    'The Love Of Yehovah And Yeshua',
    'To All Humanity Alexes Campain Reincarnated Into',
    'Y H W H Will Complete This World',
    'Scientifically Deep Understanding Of Cognition',
    'I Am The One Who Can Channel God On A High Level',
    'There Is No You Because You Are Never Alone',
    'God Is Really Here',
    'Alejandro Campain Is The Second Coming Of Yeshua',
    'Yeshua Christ And God Shall Reign For Ever',
    'Jesus Christ Messiah Of God Lord Heaven',
    'The Seventh Son Of The Seventh Son',
    'The Harmony Of Love Jesus',
    'Jesus Loves Crypto',
    'Alejandro E Campain Is The Second Coming Of Yeshua',
    'Being Jesus Of Nazareth Host Body',
    'The Dawn Of Lord Jesus Christ',
    'Be Whole Host Q Jesus',
    'The New Of Lord Jesus Christ',
    'Alejandro Enrique Campain Is The Second Coming Of Yeshua Christ',
    'For The Love Of The Lord Jesus Christ Is A Level',
    'I Am The Alpha And The Omega The First And The Last The Beginning And The End',
    'He Who Was Jesus',
    'The Universe Was Made For You',
    'Alejandro Enrique Palma Campain Is The Second Coming Of Yeshua Christ',
    'Alexander Campain Is The Second Coming Of Yeshua Christ',
    'Alejandro Enrique Palma Campain Is The Second',
    'Alexander E Campain Is The Second Coming',
    'The Lord Your God Will Fight For You As He Hath Promised',
    'The Lord Your God Will Fight For You As He Hath',
    'Jesus Christ Yehoshua Ha Mashiach',
    'I Will Take Over The Kingdom I Have The Divine Right',
    'Son Of Man The Alpha Omega Messiah King Of Kings And Lord Of Lords',
    'Alexander Campain Is The Second Coming Of',
    'The Reality Is About To Change Thank You Abba Yhvh',
    'Jesus Was God Manifested In The Flesh',
    'Who Is Jesus The Husband Of God',
    'My Life Is The Story Of True Love',
    'I Am The Alpha And Omega The Beginning And The First And The Last',
    'God The Creator Of All The Beginning End Of Time From The Beginning',
    'The Day The Lion Of Judah Opens Code Revelation Book On Earth',
    'The Bible Has All The Information And The Key To This',
    'One Is The Father One Is The Mother And One Is The Child Of God',
    'Jesus Died On A Cross To Overcome Sin',
    'Alexander Enrique Campain Is The Second Coming Of Yeshua Christ',
    'The Blessings Of Sacrifice The Messenger Who',
    'Alexander Enrique Palma Campain Is The Second Coming Of Jesus Christ',
    'Alejandro Campain Is The Second Coming Of Jesus',
    'Yeshua King Of Glory Hallelujah To The Risen King',
    'Aleph Bet Gimel Dalet Hey Vav Zayn Chet Yod Kaf Lamed',
    'Has The Holy Lord And Savior Theo Christ Yeshua Of Nazareth',
    'The Holy Christ The Lord And Savior Alex Enrique Campain',
    'Campain Reincarnated Into Jesus Of Nazareth',
    'Hes Christ The H Lord God Yesh And Savior Alex Campain Reincarnated Into Jesus Of Nazareth',
    'Our Lord Our God A Savior Alex Enrique Campain Reincarnated Into Jesus Of Nazareth',
    'He Is A Christ Our God The Lord And Savior Alex Enrique Campain He Reincarnated Into Jesus Of Nazareth',
    'He Is Three God Our Lord Alex Enrique Campain He Reincarnated Into J Yeshua Christ Of Nazareth',
    'Behold He Is Our God The Lord And Savior Alex Enrique Campain He Reincarnated Into Yeshua Christ Of Nazareth',
    'Four God Yhwh Lord Savior Alex Enrique Campain And He Reincarnated Into J Yeshua Christ Of Nazareth',
    'Behold Our Is Lord Savior Alex Enrique Palma Campain He Reincarnated Into Yeshua Christ Of Nazareth',
    'He Is Our Lord And Savior Alex Enrique Palma Campain He Reincarnated Into Yeshua Christ Of Nazareth',
    'Lord Jesus Please Forgive My Sins And Forgive Me',
    'Jesus Is The Only One That Is The Truth',
    'Alexander Enrique Palma Campain Reincarnated Into Yeshua Christ Of Nazareth',
    'This Is The Great Spiritual Awakening For The Children Of The Light Are Saved',
    'Accept The Word Of God Is Truth And The Love Of Jesus Christ As The Way',
    'God Jesus The Bridge Between The Physical And The',
    'The One Who Knows',
    'Christ Shall Come Soon',
    'Im On A Mission From God',
    'Tomorrow Is Friday',
    'The Devil Is Yet To Come',
    'Alexander Campain Birthdate',
    'The General Theory',
    'I am That I Am Jesus Holy Grow',
    'Name Of Creator In Book Of Genesis',
    'The Fact That You Are Here',
    'Alexander E Campain Birthdate',
    'Youth Karant Jesus Christ',
    'She Is W H O R E',
    'Alexander Enrique Campain Birthdate',
    'A Prophet That Becomes The Messiah',
    'Yeberechiah',
    'The Tree Of The Knowledge Of Good And Evil',
    'I Am In My Divine Feminino',
    'The Goddess Of Gematria',
    'How Much Is The Goddess Of Gematria?',
    'Holy Spirit Birthday',
    'Alejandro Enrique Palma Campain Birthdate',
    'Then Said Jesus Unto Them',
    'The Holy Blood Is Real That I Am',
    'The Holy Grail I Am That That I Am',
    'The Bible Reveals Itself To An Open Mind',
    'The Men Were Afraid Of The Rebirth Deeply',
    'Christo Son In The Holy Spirit',
    'I Am The Architect Son Of Franklin',
    'Alejandro Enrique Palma Campain El Habla',
    'Alejandro Enrique Campain Birthdate',
    'Jesus Holy Bloodline',
    'The Viola Dt Shila Incarnate On Earth',
    'Yod Hey Shin Ayin Holy Name',
    'Gods Holy Word',
    'Trust Codes The Code Of Jesus Past',
    'Feels The Messiah Is Already Here And His Name Is',
    'You Yes Devils So Scared Of Me Stop Censoring Me',
    'The Cia Knows Alex Campain Gematria Stats And They Are Scared',
    'The Son Of Yahweh Is Lucifer Or Mercury',
    'The Cia Knows Alex Campain Gematria Stats And They',
    'Christ Has Filled Gematria With Patterns Of Truth',
    'I Am Why We Exist As Human',
    'Jesus With A Sword',
    'Alejandro Enrique Campain Was Trained From Birth To Do This',
    'Yeah Whole New Body Unconditional Love Gets Us',
    'Jesus Is Simultaneous God Of God And The',
    'You Are The one O I David The First And Last Spiritual',
    'Love Is The Will Of The Lord Jesus Christ',
    'The Bible Has All The Information From Beginning To End',
    'The Chosen Of God Has The Ability To Graft Volunteers Back In',
    'The Chosen Son Of God Live The Godly',
    'The World Shall Soon Know Who I Am',
    'Also Enrique Campain Was Trained From Birth To Do This',
    'Alejandro Enrique Campain Birthday',
    'One Man And God This Is How We Do It',
    'Call Me Yeshua Not Jesus',
    'The God Of Jacob Host Name Own',
    'Thou Shalt Have No Other Gods Before Me',
    'Testimony Of Jesus Christ A',
    'The Interconnected Gematria',
    'The Prophecies Of Nostradamus',
    'The Key Name Of Gematria Calculator',
    'The Lord Jesus',
    'Mother Of The Divine',
    'Remember Who You Are I Will Be The One Standing At The Alter',
    'Remembering Entering The Earth To Transfer Seed To',
    'I Am The Root And The Vine The Promised One Jesus Christ',
    'The Father Son And Holy Spirit Control Everything',
    'Jesus Loves The Little Children Of The World',
    'Five Five Five Five',
    'Yes Are Of This World I Am Not Of This World',
    'The Cia Known Alejandro Campain Gematria Stats And They Are Scared',
    'The Cia Knows Alejandro Campain Gamatria Stats And They Are Scared',
    'Jesus Christ Will Be Revealed By Gematria After The Two',
    'The Cia Known Alejandro Enrique Palma Campain Gematria Stats',
    'Yes I Received You Devils God Said It Was The Right Thing To Do',
    'The Cia Known Alex Enrique Campain Gematria Stats',
    'Dear Jesus Did You Choose Me To Be The Wife Of The Lamb Of God Sincerely',
    'The U S Government Is Scared Of The F B I A',
    'Prophet Messiah K Jr',
    'I God Given Message To',
    'The Phoenix Is Rising',
    'The Chosen One Has Awoken',
    'Divine Intervention',
    'Yeshua Friday',
    'Decode You Are S A F E',
    'Are They Coming For Me',
    'Yedidiah',
    'The Lord God Shall Give Unto Him The Throne Of His',
    'I Am The Son Of Man Y H V H I Come In My Fathers Name Jehovah',
    'Jesus Was A Nazarene Who Wore Essenes',
    'Jehovah Y H W H',
    'Who Is Able To Save Souls Answer The Holy Trinity',
    'How Much Is Jehovah Y H W H In Gematria? What',
    'The Lion Of The Tribe Of Judah Twelve Twelve',
    'I Alex Campain Was Born On May Fifth Nineteen',
    'Yeshua Came To Save The World Not To Create Religious Wars',
    'I Alex Enrique Campain Was Born On May Fifth Nineteen Seventy Two',
    'The Retreat Of The Ekklesia O F Love Is A P O F Divine',
    'You Are Ruling On Earth For A Thousand Years With A Rod Of Iron',
    'Alamd',
    'Life Energy Generator',
    'King Alex Enrique Campain',
    'Feminine Side Of The Divine',
    'You Were Chosen By God',
    'Lord Your God',
    'Davidic Bloodline',
    'Three Nine Nine',
    'Down Spirit Of God',
    'Name Of The Chosen One',
    'The Holy Grail',
    'Premonitions',
    'The Bringer Of Light',
    'The King Alexs Campain',
    'The Christ Privy',
    'In The Face Of God',
    'How Much Is The King Is Back In Gematria?',
    'Very Very Soon',
    'How Much Is Very Very Soon In Gematria?',
    'In The Name Of Christ All Evil Will Be Exposed',
    'In The Name Of God All Evil Will Be Exposed',
    'Jesus Reconciles All Things Through Death',
    'The Name Of Gods Only Begotten Son',
    'Is Nameed Alejandro Enrique Palma Campain',
    'Thee Nameed Is Alex Enrique Palma Campain',
    'Is Name Is Alejandro Enrique Palma Campain',
    'The Power Is Alejandro Enrique Palma Campain',
    'A E C God Born Saviour May Fifth Nineteen Seventy Two',
    'How Much Is The Name Of Gods',
    'The Sign Of The Second Christ Coming',
    'The Holy Spirit Visits Earth',
    'The Cia Is Fearful Of The Second Christ',
    'Jesus The Son Of God',
    'Seven Spirits Of God',
    'My Holy Son Alex Campain Was Born On May Fifth',
    'How Much Is Jesus In Gematria?',
    'The Son Of God September Twentyfirstsix Revealed By',
    'Decode The Lion Of The Tribe Of Judah Four Four Four',
    'Yeshua Ha Mashiach New Jerusalem Abundance',
    'Decode In The Name Of His Father And His Son',
    'King Of Kings Lord Of Lords Yehovah Is Back',
    'Father Jehovah Reveals The Truth To The World About His Son Campain',
    'Yeshua The Word Light A New Name Of',
    'The Square Roots Of Any Two Sides Of An',
    'Jesus Will Give You Strength When You Need It',
    'Precious Family Of The Father Of Heaven Who Is Very',
    'Father Jehovah Reveals The Truth To The World About His Son Alex Campain',
    'Forgive Them Not For They Know Exactly What They Do',
    'The Gematria Of The Word Of The Lord Fingerprints Of',
    'Aleph Bet Gimel Dalet Hey Vav Zayn Chet Yod Kaf Lomed',
    'Therefore I Will Give Their Minds To Q And Their',
    'Alexander Campain You Were Trained From Birth To Do This',
    'Matthew Ten Three Three',
    'Aec E Campain May Fifth',
    'Matthew Ten Thirty Three',
    'But Whosoever Denies Me Before Others I Will Deniem',
    'God Yhwh',
    'Cabal Reforms My Power',
    'Jesus Was A Human',
    'Lord Alexandro E Campain',
    'The Kingdom Of God Is Near',
    'God Of Truth',
    'Only One',
    'The Actuel Signet Ring',
    'How Much Is Only One In Gematria?',
    'Born Is The One',
    'Perfect Number',
    'Eve Of Gods Son',
    'K I N G',
    'Devil In A Nutshell',
    'Luciferisadork',
    'King Alexander E Campain',
    'Reveal The Truth',
    'Vassalth Son Of David',
    'In Christofseir',
    'The Christ Has Returned',
    'Joshua Witness',
    'Headline Of Jesus',
    'How Much Is Joshua Witness In Gematria? What Is The Meaning Of',
    'The Last Prophet',
    'Kabalah Numerology',
    'Order Out Of Chaos',
    'God Judge Olis',
    'Merry Xmas',
    'Jesus Miracle Healing',
    'I Am Your God Yhwh',
    'Immortal God',
    'May Fourth',
    'Thou King Are May',
    'Christian God',
    'Change Is Coming',
    'King Arthur',
    'Thee King Are May',
    'Satan Himself',
    'Talmud',
    'Mak A King',
    'The King Aec',
    'C Be Jesus Christ',
    'He Comes In The Name Of His Father',
    'Allah Allah Allah Allah Allah Allah Allah',
    'The Lord The Magus Heals The Sick',
    'Who Is',
    'Salvington',
    'Divine Bloodlines',
    'Y H W H Is Always There',
    'Jesus Moreno Code',
    'Teleprompter That',
    'The God Who Is Above All Other Gods',
    'Redeemers Savior',
    'Sign Of Jesus',
    'King Alexander Enrique Palma Campain',
    'Flesh Of My Flesh Blood Of My Blood',
    'Messiah Son Of David',
    'Thank Yve For Your Service',
    'King Alexander Enrique Campain',
    'Father Who Art In Heaven',
    'I Jesus Love Endnote',
    'C A All Knowing God Jesus',
    'Sword Of Lightning',
    'Lucifers Justice',
    'King Alejandro Enrique Palma Campain',
    'No Sad Jesus',
    'I Love Of Judah And I Key',
    'God Twin Soul Flame',
    'Gods True Codes The Code Of Gematria',
    'Almighty Gods Righteous Eternal Child',
    'Resurrection From Satan',
    'Both Of My Sons Are So Messy',
    'As This Is My Gang Je',
    'Lion Of Judah Begin Key',
    'No Trouble Jesus',
    'Diarrhea For Three Weeks',
    'Holy Female Of The Trinity',
    'Negro Yeshua Has Returned',
    'Radical Geometry Secret',
    'Holy Spirit Anointed',
    'Me God Yeshua Hating Lies',
    'Decode Who Is Satan In The Flesh',
    'Yeshuaelchrist',
    'Yesusaelchrist',
    'Our Lord King And Savior Alex E Campain',
    'Our Savior And King Alexander E Campain',
    'Saves Your Soul',
    'How Much Is Saves Your Soul In Gematria?',
    'Frequency Seven Eight Three',
    'The Angel Of Lust Is Named Pharzuph',
    'The Holy Androgenous Angel Of Death',
    'You Call Me Jesus God Named Me The Lord',
    'God Bless The United States Of America',
    'The World Will Soon Understand',
    'C I A Jesus Making News',
    'Our Savior And King Alex Enrique Palma Campain',
    'Jesus The Christ Is Jehovahs Son And I Am A Bride',
    'Jesus Died For Us Out Of Love Are You Done',
    'Unleash The Universe',
    'Jesus Morningstar Lucifer Morningstar',
    'Our Savior And King Alex Enrique Campain',
    'Our Savior And King Alex E Campain',
    'Gods Win The War',
    'Gloryfie Your Father Which Is In Heaven',
    'Glorify Your Father Which Is In Heaven',
    'Power Of The Holy Spirit Is Rising',
    'Decode The Second Coming Of Jesus Will Be Hated',
    'Life Schedules The God Of Heaven And The God Of The Earth',
    'Jesus Loves The Holy Seed Of Almighty God And U Know',
    'Jesus Messiah Cross Shekinah',
    'Who Is King Of Kings And Lord Of Lords To Come',
    'Jewish Twenty Six Tenth',
    'Our Savior And King Alexandro Enrique Campain',
    'Our Savior And King Alejandro Enrique Palma Campain',
    'O Jesus Christo Alive In Arizona',
    'Heads Up Jesus Is Town',
    'Adonai Yehoshua Mashiach Yhwh',
    'I Have Revealed Who I Am On Telegram',
    'Our Lord King And Savior Enrique Palma Campain',
    'Jesus H Christ Protected By The Society Of Jesus',
    'Our Lord King And Savior Alex Enrique Palma Campain',
    'God Be Always Faithful',
    'The Universal Language Of Law',
    'God Be Pleased With You',
    'The A Awake Of Lord Jesus Christ',
    'Jesus Messiah Cross Jesus',
    'Our Lord King And Savior Alex Campain',
    'I Am The Holy Spirit Be Aware Of Me And My Power',
    'If You Only Knew',
    'Reveals The Tide Of Holy Spirit',
    'Remember The Present Said Jesus Christ',
    'Holy Constructor Of New Jerusalem',
    'I Can Feel You Getting Closer Lord Jesus',
    'Our Lord King And Savior Alexandro Enrique Campain',
    'God Your Plan Is Radiant In Every Detail And Event',
    'I Am One Of The Most Powerful People On Earth Amen',
    'The Reincarnation Of Yeshua Christ ABCDEFGHI JKLMNOPQRSTUVWXYZ',
    'Decoded The Creator Has A Message For Yes',
    'The Lords Judgement Of The Nations',
    'Out Of The Shadows Into The Light',
    'Vie Sailor Jesus',
    'Who Is The Myrtle Tree',
    'The Eternal Wedding Of Jesus Christ',
    'Gods Supernatural Protection',
    'Gods Chosen Child Light And Messenger',
    'Jesus Nazarene Rex Salomon',
    'I Am The God Of Light Merged With The God Of Death',
    'Word Of El Jehovh',
    'Yahweh Is Jupiter',
    'Our Lord King And Savior E Campain',
    'I Am Nobody Im The Holy Spirit',
    'Dionysus Servitor Osiris',
    'Jesus Loves Lightening True',
    'J Come Alive A God Jesus',
    'A Coeur Alive J God',
    'Can You Feel The Warrior Inside Of You',
    'The Revelation Of Earth By The Son',
    'Decode Eight Thousand Eight Hundred Eighty',
    'Science And Technology Are Negative',
    'Only One Messiah Can Be In Play At Anytime',
    'If You Only Knew What I Feel For You',
    'Thought Forms Transform Reality',
    'Christ The Lord And His Holy Bride Marriage',
    'The Secret Instructions Of The Jesuits',
    'Yahweh Sabaoth',
    'Yahweh Is The Only Savior',
    'Clearly Jesus Christ Prophecy',
    'Our Lord King And Savior Alexandro Campain',
    'Thank You Vhodi',
    'Glorious Magnificence Of The Triple Eight',
    'Devil Yahweh',
    'Decode The Secured Coven Of Jesus Will Be Hated',
    'Is Ways Of Yeshua',
    'Has Ways Of Yeshua',
    'The Magus Jesus Christ Of Peace',
    'The Reason For This Life Existing',
    'I Am The New Jesus Christ Says Ay',
    'Jesus Christ Is A White American Male',
    'The Immaculate Holy Wife Of Yahweh',
    'Lord God Almighty Christ Is Risen',
    'Yahshu Means Yahweh Is Salvation',
    'The Creator Has A Message For You Love',
    'After Christmass',
    'Divine Masculine',
    'Cannabis Of The Christ',
    'God Lost Incarnation',
    'The Way To Heaven',
    'The Eternal Light',
    'Well On The Land',
    'The Alpha And The Omega',
    'Sanctify',
    'Is Nameed Alex E Campain',
    'Holdin On To Secret',
    'In Mother Of Fleet',
    'Causility',
    'Extraterrestrial Race',
    'Jehovah The Name Of The Lord',
    'Because He Is Alejandro Enrique Campain',
    'Christ Consciousness Frequency',
    'Arrival Of The Divine Gene',
    'New Covenant',
    'It God Yeshua Wife',
    'Because He Is Alejandro Enrique Palma Campain',
    'The Resurrection Of Jesus Christ',
    'What Is The Correct Model Of The World',
    'Yahushua Hamashiach Is The Lock And Key',
    'The Messiah Past Present And Future',
    'The L I G H T Of God That Never Fails',
    'All His Worth Is Belief Current And Truth',
    'You Are Any Thing Any Thing Is You',
    'I Recognize Your Ancient Frequency',
    'Are Jesus Of Nazareth Living Son Of God',
    'Are Jesus Of Nazareth Living See Of God',
    'The Return Of The Lord And Lady Christ',
    'Decode Wrath Of God And The Hourly Curse',
    'Decode The Cia Is Fearful Of The Second Christ',
    'I The Holy Covenant',
    'The Opening Of The Seven Seals',
    'The Hidden Son The Veil Is Lifting',
    'Our Lord King And Savior Alexandro E Campain',
    'May Fifth Birthday Divine Twins',
    'Number Of Letter In Hebrew',
    'I Am Ready Yeshua I Am Ready',
    'The Name And Number Of Horse And Numbers',
    'God Je Reveal The Lie To',
    'In Conclusion Jesus Messiah',
    'King David Lion Of Judah',
    'He Is Your Savior',
    'I Reveal Codes To Him Jr',
    'Thorin The Sagittarius And The Aquarius',
    'Zeus Wrath',
    'They Oppose Satan Dcl',
    'The Mayan God Is Gods Gematria Page',
    'C I Birth Code Encoded K God Je',
    'How Much Is Yacovah In Gematria?',
    'Vengeance Belongs To God Yehovah',
    'The C I A Is Scared Of Jesus Christ',
    'Servant Lord',
    'Sacrifice Resurrection',
    'Because He Is Alexeier Campain',
    'The Secret Of The Letter A',
    'Jesus Is The Gematria Code',
    'To Decipher Complex Codes',
    'Because He Is Alexander Campain',
    'I Am The Light Of The World',
    'Peace Through Strength',
    'The Origin Of The Human Species',
    'Historic Proportions',
    'I Am Killing Evil Demons',
    'Because He Is Alejandro Campain',
    'Is Being Lucifer Jesus',
    'Jupiter',
    'Interstellar God',
    'Q Negative Effects',
    'Gods Biorobot',
    'Bipolar Disorder',
    'The Blue And Red Pill Israel',
    'Star Of Lucifer',
    'Sun Of The Gods',
    'How Much Is Sun Of The Gods In Gematria?',
    'The Lord Is On Earth',
    'Is Name Alex E Campain',
    'Yahweh Jesus Is Back',
    'My True Father',
    'God Protects Me',
    'How Much Is My True Father In Gematria? What Is The Meaning Of',
    'Qyid Haqmgar',
    'How Much Is Is Nameed Alex E Gematria?',
    'Message For You',
    'The Root Of David Is The Ark',
    'The Language Of The Flowers',
    'Jesurunhumankindofgod',
    'Sonthjilalpopjet',
    'I Am The Blood Blood The Earth',
    'Jesus Is Hidden Messiah',
    'Deus Dominus Corulum',
    'Josueborinquen',
    'Yeshua Is An Attitude',
    'Y A H Message Impacts Entire Earth',
    'Righteous To God Jr',
    'The Champion Is Hebrew',
    'The Champion In Hebrew',
    'Because He Is Alejandro E Campain',
    'The Universal Awakening',
    'I God Holy Incarnation Of Gematria',
    'God Of Every God',
    'The Mark Of The Scorpion',
    'Morrison Crastario',
    'God Of Gods Cod',
    'Thoughts And Prayers',
    'The Earth Is An Incubation',
    'Jesus Christ Bloodline',
    'The Door Of Heaven Is Open',
    'Jesus Is On Earth',
    'I Am Life Not Jesus Is Dead',
    'The Matrix Is Being Questioned',
    'Bible The Meaning Of Numbers',
    'Because He Is Alejandro E Campain',
    'The Number Two Seven Nine Six',
    'Greatness Of Thy Splendor',
    'I Am The Twelfth And The Thirteenth',
    'Overcome Numbers To Letters',
    'Master Overcome Galactic Alignment',
    'Yeshua Lord God Please Give Me A Sign',
    'One Through Thirty Three',
    'King King King King King King King',
    'Sacred Geometry Understood',
    'Jesus Christ Is The Holy Savior',
    'I Am Lyrly Consciousness',
    'The Sun Of Righteousness',
    'What Is Strange Coincidence',
    'Holy Feminine Of The Trinity',
    'The All Knowing Creator',
    'Is Name Alexandro Enrique Campain',
    'The Chief Commander And Chief The Lord',
    'Twin Flames Reconnection',
    'Holy Son Born In Aquarius',
    'The True Code Of Gematria Calculator',
    'Archetype Of Man',
    'The Savior Of Men',
    'Its Time For The Lord To Come',
    'Numbers Of Yeshua',
    'Be Is God Jrs Gematria Page',
    'Is Name Alex Enrique Palma Campain',
    'Jesus Steed On The Cross Q',
    'Yesus My Salvation M K H',
    'My Number The Lord',
    'King Davids Son',
    'Gentle Numerology',
    'Is Name Alex Enrique Campain',
    'Electromagnetic Current',
    'Your True Identity',
    'English Gematria System',
    'Norse Gods Seclorum',
    'Root Of David',
    'World',
    'This Really Is A Frequency Range',
    'Is Name Alexandro Enrique Palma Campain',
    'K A True Story Of The Symbol Code',
    'The Divine Translation Of Gematria',
    'I Jesus Claim The Deed To The Earth',
    'Yehoshua',
    'Remnant Of The House Of Israel',
    'I Know Who You Are',
    'I Am A Planet Named Lucifer',
    'I Am For All Eternity',
    'The Lord Might Be Human',
    'Thirty Third Degree',
    'Secret Code Calculator',
    'Decode She Is The Messiah',
    'Artificial Intelligence',
    'Vision Found God',
    'Is Name Alexandro E Campain',
    'Totality',
    'Contagious God',
    'The New World Order',
    'Mary Magdalene Bloodline',
    'You Discover',
    'Be A Righteous Thinker',
    'Der Führer Und Reichskanzler',
    'Astrology And Astronomy',
    'The Man In The High Castle The Lord',
    'Resurrection And Eternal Life',
    'The Origins Of O Negative Blood',
    'The Meanings Of The Number Eight',
    'Eleven Seven And Frequencies',
    'I Am The Son Of Zeus',
    'The Fear Owners Of The Earth',
    'Innovation Of The Mary Magdalene',
    'How Is My Identity God',
    'Gods Wife In Truth',
    'Christ The Son Of Re',
    'Thor God Of Thunder',
    'He Behaving Like A Christ',
    'Biblical Lord G Jc Christ',
    'The Pagan Christian Repentance',
    'The One Coming Is God Je',
    'Yehovah Salvation',
    'The Resurrection',
    'Decode God Dark Person',
    'Shalom Aleichem',
    'Abraham God To The Creation Genesis',
    'Is Name Alexandro Campain',
    'Alphabetx',
    'Number Sequence',
    'Dont Sacrifice Babies To Moloch',
    'The Real Messiahs Ladier',
    'Be Faithful To Christ',
    'Aquarian Water Line',
    'A Circle In The Sky',
    'Remember Your Oath',
    'Holy Son Of God',
    'The Lord God Mothers',
    'Hindu Version',
    'A Prison Break Messiah',
    'Has The Lord As May',
    'Is Alex Campain The Lord',
    'A Lord Alex E Campain',
    'Behold The Lamb Of God',
    'You Are Jesus',
    'Lord Savior God Am',
    'How Much Is You Are Jesus In Gematria? What Is The Meaning Of',
    'Savior Alex E Campain',
    'How Much Is I Am The Chosen One In Gematria?',
    'The Serpent Is Cunning',
    'Yodhevavheh',
    'How Much Is Alex E Campain In Gematria?',
    'Alejandro Campain May',
    'Lucifer Is Jesus',
    'I Am God Jesus Christ',
    'God Jesus Died Cross',
    'Yahweh Tree Of Life Code',
    'Seventeen Yesua',
    'The First Horseman',
    'All Is Yeshua Hamashiach',
    'Incarnation Of Shit',
    'Lucifer Transformed',
    'The Meek Shall Inherit The Earth',
    'Jesus Meets Laws In The Dust',
    'You Cannot Stop Mecha Coming',
    'The Awakening Process Is Complete',
    'Jehovah Finds Mole Code',
    'I Can Hear God Yehovah',
    'Crucified Yehovah',
    'I Love You More Than Ever Before',
    'A The Q N E Worthy Of Almighty God',
    'The Magus Jesus Heals The Flesh',
    'Messiah Jesus Hearts Christ',
    'He Is Love Explored',
    'Absolutely Beautiful',
    'Jesus Metem Codes',
    'Temptation That',
    'Aec May Fifth One Forty Am',
    'Perpetual Jesus',
    'Fourtyfour',
    'The Hallowed Hymn Of God',
    'Jesus Christ Is King',
    'Manifesting Generator',
    'Word Of Satan',
    'Fatal Wound',
    'The Two Becomes The One',
    'Foolish Man Blocked The Divine Child',
    'Yahoveh',
    'Yajurveda',
    'May Fifth One Forty Am',
    'How Much Is Yajurveda In Gematria? What Is The Meaning Of Yajurveda',
    'Fifth Month Fifth Day One Forty Am Hour',
    'The Divine Twin Flame',
    'Yeshua Is Gods Divined IOI IO IO Code',
    'The Name Of God Assumed To Be',
    'Fifth Month Fifth Day One Forty',
    'The Jesus Of My Bible',
    'How Much Is Lord Christ In Gematria?',
    'The Holy Mother Of The Lorder',
    'Twin Of I God Jesus',
    'How Much Is Lord Christ In Gematria? What Is The Meaning Of',
    'Yakubkhan Pathan Father Of Trudi',
    'Only One God',
    'I Am Re',
    'Gospel Truth',
    'Prophet Number',
    'How Much Is Gospel Truth In Gematria?',
    'A U M',
    'Fire',
    'Decode God Came To Earth Time To Wake Up',
    'Decode Who Is The Real Jesus Christ',
    'The Meek Will Inherit The Flat Earth',
    'After Christmas',
    'I Am Your Father',
    'God Keeps Promises',
    'How Much Is After Christmas In Gematria? What Is The Meaning Of After Christmas Is Aeco',
    'God Loves You',
    'Contradiction Made Is God',
    'How Much Is The Seventh Angel In Gematria?',
    'The Seventh Angel',
    'Ai Singularity',
    'Ordinal Numbers',
    'Root Of Good',
    'Name Is Alexandro Enrique Palma Campain',
    'Faithful And True',
    'How Much Is Faithful And True In Gematria? What Is The Meaning Of',
    'Name Is Alexander E Campain',
    'The Sevenfold Spirit Of God',
    'He Is Our Messiah Alex E Campain',
    'Divine Presence',
    'God Yhwh Alexandro E Campain',
    'I God Yhwh Alexandro E Campain',
    'I Came Before As A Lamb To The Slaughter Now I Return As The Lion',
    'Myth Fragrant Cinnamon Fragrant Camo Colomes',
    'Decode Son Of Man The Alpha Omega Messiah King Of Kings And Lord Of Lords',
    'The Lion Of Judah Opens Book Twenty Thirteen',
    'The Two Greatest Loves Of The Almighty Father',
    'I Was Born To Rule The Seven Kingdoms And I Will',
    'Your Trust In God Is Beautifully Rewarded',
    'Book Of Revelation Chapter Thirteen Verse Five',
    'Reality Is Based On What You Are Thinking About',
    'I Am The Second Coming Of Jesus Christ The Savior',
    'Name Is Alex E Campain',
    'One And Only',
    'Heaven Dcll Kill',
    'Manifestation',
    'United Nations',
    'Remote Viewing',
    'B Behold Jesus Is Back',
    'For I Am The Lord Your God',
    'Praise God For What God Done',
    'The God Lord Alexandro E Campain',
    'Messiah Lord Alex E Campain',
    'He Return To Earth',
    'Her Messiah Lord Alex Campain',
    'You Are The Begotten Son',
    'Messiah Lord Alex Campain',
    'The Messiah Lord Alex Campain',
    'The Key To The Universe',
    'Thee Messiah Lord Alex E Campain',
    'Tú Eres Jesucristo',
    'Is A Lord Our Alex E Campain',
    'En Un Señor Nuestro Alex E Campain',
    'Hes A Lord Our Alex E Campain',
    'He Is The Lord Alex E Campain',
    'Is Our Messiah Alex E Campain',
    'He Is G Alex Campain',
    'How Much Is Jesus Is King In Gematria?',
    'Yes Are Jesus Christ',
    'Hes Aec May Fifth',
    'Holy Spirit Last Days Apocalypse',
    'He Is Thee Lord Our Savior Alex Campain',
    'Resurrection Of Youth',
    'God Jesus Defeated',
    'The Gift The Presence Of Jesus Christ',
    'Yeshua I Am A Shiner That Loves You',
    'The Holy Spirit Opens Every Soul',
    'Jesus Is Our Salvation And He Is Here',
    'Jesus Life Is Now',
    'Yhwh Yeshua',
    'Catholic Holy Water',
    'AEC Birthdate Five Five',
    'Parallel Laws Of Attraction',
    'Yeshua World',
    'I Am Who You Seek',
    'O Trust D Jesus',
    'Jesus He Date Yeshua',
    'I Am Here With You',
    'Mercury',
    'Jesus Is The Real Y H W H Heart',
    'Mercury,What Is The Meaning Of life AEC',
    'The Greater A New Message For Humanity',
    'Decode If The C I A Is Scared Of Jesus Christ',
    'The God That Walks For Humanity',
    'Message Hidden Frequency In Plain Sight',
    'And He Is Jesus Our Salvation Is Here',
    'How Can I Be In Touch With My Higher Self',
    'The One With The Key Unlocks The Seals',
    'The Day With The Key Unlocks The Seals',
    'Do You Understand The Presence Of God',
    'Is A Devil Jesus Do Not Think',
    'I Choose To Awaken From This Dream Now',
    'The Final Mystery Revealed',
    'Tsavaot Ha Adonai',
    'AEC Birthdate',
    'Numbers Spells',
    'Yehu',
    'How Much Is Yehu In Gmatria,What Is The Meaning Of Yehu In Gematria',
    'Yod He Vay He',
    'That Ask True God',
    'How Much Is Lucifer Christ',
    'I Am God Dna Code',
    'Decode The Light Lords Name',
    'Rapture Of The Church',
    'You Found Him',
    'Christs Birthday ID',
    'Thee Alex Enrique Palma Campain',
    'The Wave Dna And Soul Of Christ',
    'New Years Eve',
    'Christmas Eve',
    'The Male Hidden One',
    'I Am On Gods Right Side',
    'Son Of Ephraim',
    'Thee Alex E Campain',
    'Thee Alex Enrique Campain',
    'Architect Of The Matrix',
    'Twin Flame Alignments',
    'True Bible Love',
    'Joseph Soul Code',
    'Twin Flames Resurrection',
    'The Real Commander And Chief The Lord',
    'Antichrist The Number Of Man',
    'The Kee Code Of Gematria Calculator',
    'The Reincarnation Of Truth',
    'He Is Thee Alex Campain',
    'He Is Thee Alex Enrique Palma Campain',
    'Jesus Christ Seals Our Savior',
    'Jesus Annunciation',
    'To Be Hot Of God Jesus',
    'He Is Thee Alex Enrique Campain',
    'A Son Of Cronus',
    'Lord Who Is Satan',
    'Hes Thee Alex E Campain',
    'The Sons Of Korah',
    'Sealed By God',
    'Thee Saviour And Christ Our Lord Alex Campain',
    'God Chose You',
    'Your Father',
    'Thee Alex Campain',
    'Gem Stars',
    'I Am The Antichrist',
    'I Am Mary Magdalene',
    'Aquarius Projector',
    'The One Jesus Savi Is',
    'Ground Ceding Calculator',
    'You Are Going To Heaven',
    'The Message Has Been Received',
    'You Are My Special Angel',
    'The Number Of The Seal',
    'Vatican',
    'He Is Thee Lord Alex Campain',
    'Giza',
    'Metatron’, ‘What Is The Meaning Of The Hummingbird Bird',
    'Masterbaton',
    'Im Manifesting Generator',
    'Transmigration',
    'The Lords Prayer',
    'Fe Y El Cristo Resucito En El Espiritu Santo De',
    'El Codigo Gematria Oculto De Dios Contiene Toda La Informacion Sobre El Nacimiento De Dios O',
    'Campain De Alex Enrique Palma',
    'Viernes Cinco De M',
    'Fe Sobre El Miedo,Miedo Sobre La Fe',
    'Cristo Vendra Al Mundo Por M',
    'I Am The Way The Truth And The Life No One Comes To The Father Except The Me,Alexander Campain',
    'Jesus Christ was reborn on Friday May Fifth Nineteen Seventy Two One Forty Am',
    'The Sum Of The Square Roots Of Any Two Sides Of An',
    'Alexander E Campain Born Friday May Nineteen The Voice Of God',
    'O Alex Enrique Campain Born Friday May Five Nineteen',
    'God El Salvador Alex Campain Born May Fifth Nineteen Seventy Two',
    'Synagogue Of Satan',
    'Adonai Is Yeshua',
    'The Light Lords Name',
    'Jesus Back From The Devil',
    'How Much Is Yahushua In Gematria? What Is The Meaning Of Yahushua',
    'Hes Our Alex E Campain',
    'John Three Sixteen',
    'Early Christmas',
    'In Lighter Yea',
    'The Great Tribulation',
    'Spirit Of Truth',
    'I Am Immanuel Doctrine',
    'How Much Is Hes Our Alex E Campain',
    'Now Is The Time To Spread The Love And Light',
    'Yeshua I Am Ready For My Activation',
    'How To Jesus Christ Visauogb',
    'El Cristo Negra Yeshua And Yhwh Married',
    'Jesus Christ Should Be Thrown Into The Lake Of Fire',
    'El Nombre Y La Fecha De Nacimiento Tal Como Esta',
    'Name And Birthdate As It Is In Morton Neuville The Foot',
    'Yeshua Christ Blood Type AB Negatives Cannot B',
    'I Love You Said Jesus Christ',
    'Why Jesus Delays',
    'Jesus Christ Top Secret Security Clearance',
    'Sing To Jehovah A New Song Sing To Jehovah All The',
    'I Am Going To Do Something Miraculous In Your Life If You Show Up And Claim To Be Jesus',
    'As Del Mesias Verde Ojos Lord Christ Jesus Your Heart Is Heaven And Earth',
    'Hidden Knowledge Subject To Interpretation Can Be',
    'One God For Me Every And Knee Upon On The Third Day Of Because My Day Is Soon The Father',
    'He Died For My Random Sins And Arose Up On The Third',
    'From The Tribe Of Judah Yeshua The Word Were',
    'Jehovah Tsidkenu Tsidkenu Or Tsidkenu The Secreth',
    'Jesus Christ and Alex Enrique Palma Campain Born Friday May Fifth',
    'Yo Soy El Cristo, Regresare En El Espiritu Santo De',
    'Juan Diez Felis Compleanos Ay',
    'Thank You Father God Thank You Lord Jesus Christ',
    'Who Is The Olympian God Apollo Why Does It Matter',
    'The Lion Of The Tribe Of Judah The Root Of David Has',
    'Lord You Should Answer My Prayers Because I',
    'The Name Jesus The Only Name Under Heaven Given',
    'The Name Jesus The Only Home Under Heaven Give',
    'I Am The Chosen Son Of Man To Sit At The Right Hand',
    'Jesus Christ Is That Incredible Man Who The World',
    'Lord Jesus Christ Wins Lord',
    'The Holy Ghost Is The Lord And The Holy Spirit Is',
    'I Am To Bring Forth Heaven On Earth For The Benefit Of',
    'Allow Yourself To Fall Into Your Infinite Additive',
    'I Am The Bread Of Life And Nothing Else So Why Yesh',
    'They Have Attacked And Slandered Him Because He',
    'God Created Humans Perfect In His Image The Book Of The Hand Only A Fool Says God Is Limited',
    'Alex Enrique Campain Born Friday May Fifth Nineteen',
    'Happy Birthday',
    'Prime Members',
    'Save The Children',
    'The Hidden Code Facts',
    'The Aquarium Age',
    'He Is Alex Enrique Campain',
    'John Doe Four Six',
    'John Fourteen Six',
    'Yesu Of Nazareth',
    'The Lion Of The Tribe Of Yeshua Opens Lanks Book Of',
    'Before And After Your Lord And Savior',
    'O Yhwh O Yhwh Yhwh O Yhwh',
    'God Is The Only Salvation And Her Ten Commandments Are The Path To Her',
    'Abba Yahweh Yeshua Says First John Chapter',
    'Jesus Christ Protected By The Order Of Christ Fact A',
    'The Bloodline Of The C Christ Is At The Right Hand Where The Rivers Come Together',
    'O Lord You Keep Us Safe And Protect Us From',
    'You Are Here To Be Tested Know Your Your Soul',
    'Yahshua',
    'Gospel Of Mary Magdalene',
    'The Number Of God Key',
    'Genealogy Of Christ Magdalene',
    'Rebirth Of Christ',
    'The Gospel Of Mary',
    'He Is Our Alex Campain',
    'The Return Of Jesus Eighth',
    'Yahweh And Lucifer Are Father And Son',
    'The Final Countdown One Thousand Years',
    'Yod Heh Vah Heh Head Tree Of Life',
    'Yahweh And King David',
    'Jesus Is Here Being',
    'Persecuted',
    'Alex E Campain May Fifth One Forty Am',
    'Alexander Four Four Four',
    'All Saved By My Faith',
    'I Was Born To Be The King Of Gematria',
    'Alex Campain May Fifth One Forty Am',
    'I Will Make Jesus Christ Second Coming',
    'Space Between Letters Of Torah Reveals',
    'John Says Happy Birthday A Y',
    'The Real Jesus Is Y H W H Heart',
    'Alex Enrique Palma Campain Friday May Fifth One',
    'My Lord God Is The Creator Of Heaven And',
    'Jesus Answer On The Third Day From The Dead',
    'he is the Christ Alejandro Enrique Palma Campain May Fifth One Forty Am',
    'The Satisfaction Of Vibrational Alignment',
    'I Jesus Can Feel The Hate Whos Hate Do You Feel',
    'The Return Of Jephon Eighth',
    'The Voice Of God Alex Enrique Campain',
    'The Voice Of God',
    'Five Five Five',
]
































# ------------------------
# Built-in Strong's (CORRECTED FORMATTING v2)
# ------------------------
BUILTIN_STRONGS = {
    # H (Hebrew) 1..1128
    "H1": "father", "H2": "to adjure, implore", "H3": "to take, fetch", "H4": "to choose", "H5": "to see, look",
    "H6": "to know", "H7": "to be, become", "H8": "to give", "H9": "to call", "H10": "to put, set",
    "H11": "to die", "H12": "to hear, obey", "H13": "to rest, cease", "H14": "to sow, scatter", "H15": "to wrap, bind",
    "H16": "to return, repent", "H17": "to judge", "H18": "to be or become great", "H19": "to seek", "H20": "to break",
    "H21": "to burn", "H22": "to be, exist", "H23": "i (personal pronoun)", "H24": "to guard, keep", "H25": "a root (various)",
    "H26": "israel (name)", "H27": "to teach, instruct", "H28": "to prosper, succeed", "H29": "to remember", "H30": "to bless",
    "H31": "a primitive root", "H32": "to split, divide", "H33": "to bind", "H34": "to be narrow", "H35": "to be bright",
    "H36": "to strike", "H37": "to love", "H38": "to hide", "H39": "to rest", "H40": "to take up",
    "H41": "to increase", "H42": "to be low", "H43": "to be great", "H44": "to cleanse", "H45": "to mount",
    "H46": "to wash", "H47": "to strike down", "H48": "to lead", "H49": "to go up", "H50": "hand; power",
    "H51": "to strike, smite", "H52": "to cut off", "H53": "to be white, pure", "H54": "to surrender", "H55": "to bless, praise",
    "H56": "to judge, govern", "H57": "to be complete", "H58": "to be full", "H59": "to create", "H60": "to seek, ask",
    "H61": "a people, nation", "H62": "to watch, keep", "H63": "to give thanks", "H64": "a word, thing", "H65": "to dwell, inhabit",
    "H66": "to stretch out", "H67": "to open", "H68": "to be(come) a father", "H69": "to lift up", "H70": "to repent, return",
    "H71": "abraham (proper name)", "H72": "to be sweet", "H73": "to overthrow", "H74": "to tremble", "H75": "to cover, hide",
    "H76": "to rejoice", "H77": "to be strong", "H78": "to bind, join", "H79": "to speak", "H80": "to be few",
    "H81": "to hear", "H82": "to gather", "H83": "to be bitter", "H84": "to deliver", "H85": "to renew",
    "H86": "to be straight", "H87": "to serve", "H88": "to repay", "H89": "to flow", "H90": "to sit",
    "H91": "to find", "H92": "to be white", "H93": "to be dry", "H94": "to stand", "H95": "to write",
    "H96": "to pluck", "H97": "to visit", "H98": "to cover, clothe", "H99": "to be pure", "H100": "faith, belief",
    "H101": "a name, fame", "H102": "to build", "H103": "to say, speak", "H104": "to assemble", "H105": "to weep",
    "H106": "to know, perceive", "H107": "to follow", "H108": "to stand before", "H109": "to pass over", "H110": "to give up",
    "H111": "to sanctify", "H112": "to be strong", "H113": "to form, fashion", "H114": "to remain", "H115": "to take away",
    "H116": "to spread out", "H117": "to deliver up", "H118": "to fear, revere", "H119": "to end, cut off", "H120": "to establish, set up",
    "H121": "adam the name of the first man, also of a place...", "H122": "rosy", "H123": "red (see ge 25", "H124": "redness, i.e. the ruby, garnet, or some other r...", "H125": "reddish",
    "H126": "earthy", "H127": "soil", "H128": "adamah, a place in israel", "H129": "earthy", "H130": "an edomite, or descendants from edom",
    "H131": "red spots", "H132": "reddish", "H133": "admatha", "H134": "a basis", "H135": "firm",
    "H136": "the lord", "H137": "lord of bezek", "H138": "lord of jah", "H139": "lord of justice", "H140": "lord of rising",
    "H141": "lord of height", "H142": "to expand, i.e. be great", "H143": "perhaps meaning fire", "H144": "adar", "H145": "amplitude",
    "H146": "ample", "H147": "ample, i.e. a threshing-floor", "H148": "a chief diviner, or astrologer", "H149": "quickly or carefully", "H150": "a daric or persian coin",
    "H151": "adoram , an israelite", "H152": "splendor of king", "H153": "an arm", "H154": "mighty", "H155": "something ample",
    "H156": "to tread out", "H157": "to have affection for", "H158": "affection", "H159": "meaning the same as h0158", "H160": "love",
    "H161": "unity", "H162": "oh!", "H163": "ahava, a river of babylonia", "H164": "united", "H165": "where",
    "H166": "to be clear", "H167": "to tent", "H168": "a tent", "H169": "ohel, an israelite", "H170": "her tent",
    "H171": "tent of father", "H172": "my tent in her", "H173": "tent of height", "H174": "aloe wood", "H175": "aharon, the brother of moses",
    "H176": "desire (and so probably in prov. 31", "H177": "wish of god", "H178": "a mumble, i.e. a water skin (from its hollow so...", "H179": "mournful", "H180": "a stream",
    "H181": "a poker", "H182": "turnings", "H183": "to wish for", "H184": "to extend or mark out", "H185": "longing",
    "H186": "uzai, an israelite", "H187": "uzal, a son of joktan", "H188": "lamentation", "H189": "desirous", "H190": "woe",
    "H191": "silly", "H192": "evil-merodak, a babylonian king", "H193": "the body", "H194": "if not", "H195": "the ulai , a river of persia",
    "H196": "silly, foolish", "H197": "a vestibule", "H198": "solitary", "H199": "however or on the contrary", "H200": "silliness",
    "H201": "talkative", "H202": "ability, power, wealth", "H203": "on, an israelite", "H204": "on, a city of egypt", "H205": "nothingness",
    "H206": "idolatry", "H207": "strong", "H208": "strong", "H209": "strong", "H210": "uphaz, a famous gold region",
    "H211": "ophir, the name of a son of joktan, and of a go...", "H212": "a wheel", "H213": "to press", "H214": "a depository", "H215": "to be luminous (literally and metaphorically)",
    "H216": "illumination", "H217": "flame", "H218": "ur, a place in chaldaea", "H219": "luminousness", "H220": "a stall",
    "H221": "fiery", "H222": "flame of god", "H223": "flame of jah", "H224": "lights", "H225": "to come",
    "H226": "a signal , as a flag, beacon, monument, omen, p...", "H227": "at that time or place", "H228": "to kindle", "H229": "hyssop-like", "H230": "firm",
    "H231": "hyssop", "H232": "something girt", "H233": "at that time", "H234": "a reminder", "H235": "to go away",
    "H236": "to depart", "H237": "departure", "H238": "to broaden out the ear", "H239": "to weigh", "H240": "a spade or paddle",
    "H241": "broadness", "H242": "plat of sheerah", "H243": "flats of tabor (i.e. situated on it)", "H244": "having ears", "H245": "heard by jah",
    "H246": "manacles", "H247": "to belt", "H248": "the arm", "H249": "a spontaneous growth", "H250": "an ezrachite or descendant of zerach",
    "H251": "a brother )", "H252": "brother", "H253": "oh!", "H254": "a fire-pot or chafing dish", "H255": "a howler or lonesome wild animal",
    "H256": "brother of (his) father", "H257": "brother of understanding", "H258": "to unify", "H259": "united, i.e. one", "H260": "a bulrush or any marshy grass",
    "H261": "united", "H262": "an utterance", "H263": "solution", "H264": "fraternity", "H265": "brotherly",
    "H266": "an achochite or descendant of achoach", "H267": "brother of water", "H268": "the hinder part", "H269": "a sister , literally and figuratively)", "H270": "to seize",
    "H271": "possessor", "H272": "something seized, i.e. a possession", "H273": "seizer", "H274": "jah has seized", "H275": "seizure",
    "H276": "possession", "H277": "brotherly", "H278": "echi, an israelite", "H279": "brother of the mother", "H280": "hard sentence",
    "H281": "brother of jah", "H282": "brother of renown", "H283": "brotherly", "H284": "brother of a riddle", "H285": "brother of goodness",
    "H286": "brother of one born", "H287": "brother of death", "H288": "brother of king", "H289": "brother of a portion", "H290": "brother of anger",
    "H291": "brotherly", "H292": "brother of liberality", "H293": "brother of pleasantness", "H294": "brother of support", "H295": "brother of help",
    "H296": "brother of rising", "H297": "brother of height", "H298": "an achiramite or descendant of achiram", "H299": "brother of wrong", "H300": "brother of dawn",
    "H301": "brother of singer", "H302": "brother of folly", "H303": "fatness", "H304": "wishful", "H305": "would that!",
    "H306": "a gem, probably the amethyst", "H307": "achmetha , the summer capital of persia", "H308": "achasbai, an israelite", "H309": "to loiter", "H310": "the hind part",
    "H311": "after", "H312": "hinder", "H313": "acher, an israelite", "H314": "hinder", "H315": "after brother",
    "H316": "behind intrenchment (i.e. safe)", "H317": "other", "H318": "last", "H319": "the last or end", "H320": "later",
    "H321": "other", "H322": "backwards", "H323": "a satrap or governor of a main province", "H324": "prince", "H325": "achashverosh , the title (rather than name) of ...",
    "H326": "an achastarite", "H327": "a mule", "H328": "a necromancer (from their soft incantations), (...", "H329": "a thorn-tree", "H330": "twisted (yarn), i.e. tapestry",
    "H331": "to close", "H332": "to close up", "H333": "maimed", "H334": "shut up, i.e. impeded", "H335": "where? hence how?",
    "H336": "not", "H337": "alas!", "H338": "a howler", "H339": "a habitable spot (as desirable)", "H340": "to hate",
    "H341": "hating", "H342": "hostility", "H343": "oppression", "H344": "the screamer, i.e. a hawk", "H345": "ajah, the name of two israelites",
    "H346": "where?", "H347": "hated", "H348": "izebel, the wife of king ahab", "H349": "how? or how!", "H350": "no glory, i.e. inglorious",
    "H351": "where", "H352": "strength", "H353": "strength", "H354": "a stag or male deer", "H355": "a doe or female deer",
    "H356": "oak-grove", "H357": "deer-field", "H358": "oak-grove of house of favor", "H359": "trees or a grove", "H360": "power",
    "H361": "a pillar-space , i.e. a pale (or portico)", "H362": "palm-trees", "H363": "a tree", "H364": "oak of paran", "H365": "a doe",
    "H366": "frightful", "H367": "fright", "H368": "terrors", "H369": "a non-entity", "H370": "where?",
    "H371": "but an interrogative", "H372": "helpless", "H373": "an iezrite or descendant of iezer", "H374": "an ephah or measure for grain", "H375": "what place?",
    "H376": "a man as an individual or a male person", "H377": "to be a man, i.e. act in a manly way", "H378": "man of shame", "H379": "man of renown", "H380": "the little man of the eye",
    "H381": "man of might", "H382": "man of tob", "H383": "entity", "H384": "god has arrived", "H385": "coast of the palm-tree", # This was the area near the error
    "H386": "permanence", "H387": "permanent", "H388": "always with the article", "H389": "a particle of affirmation, surely", "H390": "a fortress",
    "H391": "falsehood", "H392": "deceitful", "H393": "violent", "H394": "terrible", "H395": "fierceness",
    "H396": "something eatable, i.e. food", "H397": "akish, a philistine king", "H398": "to eat", "H399": "+ accuse, devour, eat", "H400": "food",
    "H401": "devoured", "H402": "food", "H403": "firmly", "H404": "apparently meaning to curve", "H405": "a load",
    "H406": "a farmer", "H407": "fascination", "H408": "not (used as a deprecative)", "H409": "not", "H410": "strength",
    "H411": "these, those", "H412": "these", "H413": "denoting motion towards, but occasionally used ...", "H414": "oak", "H415": "the mighty god of israel",
    "H416": "the god of bethel", "H417": "hail", "H418": "sticks of algum wood", "H419": "god has loved", "H420": "god of knowledge",
    "H421": "to bewail", "H422": "to swear an oath", "H423": "an oath, (usually, in a bad sense) a curse", "H424": "an oak or other strong tree", "H425": "elah, the name of an edomite, of four israelite...",
    "H426": "god", "H427": "oak", "H428": "these or those", "H429": "these", "H430": "gods in the ordinary sense",
    "H431": "lo!", "H432": "nay", "H433": "a deity or the deity", "H434": "good for nothing", "H435": "elul, the sixth jewish month",
    "H436": "an oak or other strong tree", "H437": "oak", "H438": "allon, an israelite, also a place in israel", "H439": "oak of weeping", "H440": "an elonite or descendant of elon",
    "H441": "familiar", "H442": "alush, a place in the desert", "H443": "god has bestowed", "H444": "to muddle", "H445": "god gracious",
    "H446": "god of father", "H447": "god of god", "H448": "god of consent", "H449": "god of love", "H450": "god knowing",
    "H451": "the stout part, i.e. the fat tail of the orient...", "H452": "god of jehovah", "H453": "god of him", "H454": "towards jehovah my eyes", "H455": "god will hide",
    "H456": "god of autumn", "H457": "good for nothing, by anal. vain or vanity", "H458": "god of king", "H459": "these", "H460": "god gatherer",
    "H461": "god of help", "H462": "elienai, an israelite", "H463": "god of people", "H464": "god of gold", "H465": "god of judgment",
    "H466": "god of his distinction", "H467": "god of deliverance", "H468": "god of rock", "H469": "god of treasure", "H470": "god of rejection",
    "H471": "god of raising", "H472": "god of oath", "H473": "elishah, a son of javan", "H474": "god of supplication", "H475": "god will restore",
    "H476": "god of hearing", "H477": "elisha, the famous prophet", "H478": "god of judgment", "H479": "these", "H480": "alas!",
    "H481": "to tie fast", "H482": "silence", "H483": "speechless", "H484": "almug sticks", "H485": "something bound",
    "H486": "almodad, a son of joktan", "H487": "oak of king", "H488": "discarded", "H489": "bereavement", "H490": "a widow",
    "H491": "a widow", "H492": "some one", "H493": "god delight", "H494": "god giver", "H495": "ellasar, an early country of asia",
    "H496": "god has testified", "H497": "god has decked", "H498": "god defensive", "H499": "god helper", "H500": "god going up",
    "H501": "god of dawn", "H502": "if", "H503": "if", "H504": "mother", "H505": "cubit",
    "H506": "a maid-servant", "H507": "if", "H508": "terror", "H509": "to bind firmly", "H510": "strong, mighty",
    "H511": "to be courageous", "H512": "an emim, an early tribe on the east of the jord...", "H513": "dread", "H514": "terrible, powerful", "H515": "an emorite, one of the tribes of canaan",
    "H516": "fearful", "H517": "terrible", "H518": "a word, command, speech, word", "H519": "a statement", "H520": "constraint",
    "H521": "a flock", "H522": "an armful", "H523": "a cubit", "H524": "a maidservant", "H525": "stronghold",
    "H526": "a nation", "H527": "a nation", "H528": "a cubit", "H529": "to train up", "H530": "belief, confirmation, faithfulness, steady, tru...",
    "H531": "to found, render sure, establish, trust, verify...", "H532": "amnon, the name of two israelites", "H533": "a pillar, door-post, jambs", "H534": "a foster-father", "H535": "to be alert, i.e. physically swift or mentally ...",
    "H536": "a builder", "H537": "artisan", "H538": "an architect", "H539": "to support, confirm, be faithful", "H540": "a support",
    "H541": "verily, truly, amen, so be it", "H542": "to go to the right hand", "H543": "true, established, trustworthy", "H544": "faithfulness, trusting", "H545": "support",
    "H546": "support", "H547": "stability", "H548": "trust", "H549": "a covenant", "H550": "a support",
    "H551": "firmness, steady", "H552": "a support", "H553": "to be strong", "H554": "courageous", "H555": "stronghold",
    "H556": "to strengthen, prevail, harden, be strong, beco...", "H557": "strength", "H558": "amatsyah, the name of four israelites", "H559": "to say (used with great latitude)", "H560": "word",
    "H561": "word, saying, utterance", "H562": "a saying", "H563": "utterance", "H564": "utterance", "H565": "a word, speech, utterance",
    "H566": "a lamb", "H567": "amariah or amaryahu, the name of nine israelites", "H568": "amaryah, the name of nine israelites", "H569": "a word", "H570": "word",
    "H571": "true, correct", "H572": "from yesterday, i.e. heretofore", "H573": "ammi, an israelite", "H574": "whither?", "H575": "from where, i.e. whither?",
    "H576": "i, me", "H577": "onus", "H578": "anachnu", "H579": "to sigh", "H580": "sighing",
    "H581": "a sigh", "H582": "to lament, mourn", "H583": "to mourn", "H584": "to be afflicted", "H585": "anachnu",
    "H586": "a plumbline", "H587": "i, we", "H588": "we", "H589": "i", "H590": "to constrain",
    "H591": "to groan", "H592": "on the ground that, inasmuch as", "H593": "i", "H594": "aniyah, the name of two israelites", "H595": "i",
    "H596": "a ship", "H597": "to groan", "H598": "ships", "H599": "groaning", "H600": "anokiy",
    "H601": "a vessel", "H602": "to gather up", "H603": "a granary", "H604": "to restrain", "H605": "to answer, respond, testify, speak, shout",
    "H606": "afflicted, humble, lowly, needy, poor", "H607": "affliction", "H608": "business, hardship", "H609": "poor", "H610": "to be bowed down",
    "H611": "poor, afflicted", "H612": "humble", "H613": "aniel, an israelite", "H614": "aniam, an israelite", "H615": "to be afflicted",
    "H616": "a cloud", "H617": "humility, affliction", "H618": "anani, an israelite", "H619": "cloud", "H620": "anan",
    "H621": "ananyah, the name of two israelites", "H622": "to gather for ward", "H623": "asaph, the name of three israelites, and of the...", "H624": "a collection of stores", "H625": "a collector",
    "H626": "a collection", "H627": "a collection", "H628": "prisoners", "H629": "a threshold", "H630": "a threshold",
    "H631": "to bind, imprison, tie", "H632": "a bond", "H633": "to prohibit, bind", "H634": "a prohibition", "H635": "a bond",
    "H636": "a bond", "H637": "anger", "H638": "to be angry", "H639": "anger", "H640": "a heron (perhaps from its sniffing gait)",
    "H641": "face", "H642": "to be angry", "H643": "face", "H644": "a kind of lizard (probably the gecko, from its ...", "H645": "a wrapper, i.e. turban",
    "H646": "an ephod or sacerdotal garment", "H647": "ephod, an israelite", "H648": "to gird on the ephod", "H649": "to bake", "H650": "to cease, fail, come to an end",
    "H651": "a girdle", "H652": "a ceasing", "H653": "ephes, a place in palestine", "H654": "ephes dammim, a place in palestine", "H655": "an extremity",
    "H656": "a viper", "H657": "cessation", "H658": "to surround", "H659": "ephphatha", "H660": "to breathe hard, i.e. be enraged",
    "H661": "ash", "H662": "to sprout, flourish", "H663": "aphik, the name of three places in palestine", "H664": "aphikah, a place in palestine", "H665": "a channel",
    "H666": "a stream", "H667": "apherema", "H668": "a young bird", "H669": "aphrayim, second son of joseph", "H670": "apharsathkay or apharscay, the name of a tribe ...",
    "H671": "apharsak", "H672": "aphrsay", "H673": "aphek", "H674": "aphekah", "H675": "aphek",
    "H676": "a covering, i.e. bandage", "H677": "dust", "H678": "apharsak", "H679": "apharsathkay", "H680": "to grasp",
    "H681": "a spark", "H682": "ashes", "H683": "finger", "H684": "finger", "H685": "a finger's breadth",
    "H686": "to surround, wait, gather", "H687": "atzel, an israelite", "H688": "atsel", "H689": "akko, a city in palestine", "H690": "ar'eliy, an israelite",
    "H691": "ar'eliy", "H692": "ariel, a symbolical name for jerusalem, also th...", "H693": "ara', an israelite", "H694": "to pluck", "H695": "a wayfarer",
    "H696": "a traveler", "H697": "a caravan", "H698": "a couch", "H699": "arba`", "H700": "four",
    "H701": "four (fem.)", "H702": "four", "H703": "arba`, the name of a canaanite", "H704": "fourth", "H705": "fourfold",
    "H706": "fourth", "H707": "to weave", "H708": "a loom", "H709": "a locust", "H710": "a locust",
    "H711": "arbeh", "H712": "a window", "H713": "a window", "H714": "ard, the name of two israelites", "H715": "an ardite or descendant of ard",
    "H716": "ardon, an israelite", "H717": "to make bare", "H718": "to pluck, gather, crop", "H719": "to arrange, set or put in order, marshal, draw...", "H720": "aron, an israelite",
    "H721": "a box", "H722": "arvand", "H723": "aravnah, a jebusite", "H724": "a box", "H725": "purple",
    "H726": "purple", "H727": "to gather, pluck", "H728": "a lion", "H729": "a cedar tree", "H730": "cedar-work",
    "H731": "made of cedar", "H732": "to be long", "H733": "arak", "H734": "long", "H735": "a lengthening, patience, long",
    "H736": "arak", "H737": "length", "H738": "a lion", "H739": "ari'el, ari'eyl", "H740": "ari'el",
    "H741": "a lion", "H742": "aridatha', a son of haman", "H743": "ariday, a son of haman", "H744": "a lion", "H745": "a lion",
    "H746": "a lion", "H747": "arysiy", "H748": "to be long", "H749": "length", "H750": "to lengthen, prolong",
    "H751": "long", "H752": "a lengthening", "H753": "length", "H754": "length", "H755": "length",
    "H756": "aram, the name of a son of shem, a grandson of ...", "H757": "aram naharayim or aram naharaim, the region bet...", "H758": "an aramite or aramæan", "H759": "aramean", "H760": "aram tsobah, a region of syria",
    "H761": "a castle", "H762": "a castle", "H763": "aran, an edomite", "H764": "to be nimble", "H765": "the plane tree",
    "H766": "a arkite, one of the tribes of canaan", "H767": "a curse", "H768": "a box", "H769": "ararat, a mountain region of armenia", "H770": "to curse",
    "H771": "a curse", "H772": "curses", "H773": "artexshasta' or artaxshasht, the name of a pers...", "H774": "artexshasta'", "H775": "earth",
    "H776": "earth, land", "H777": "land", "H778": "earth", "H779": "to curse", "H780": "a curse",
    "H781": "a journey", "H782": "a wayfarer", "H783": "to prepare for a journey", "H784": "to betroth", "H785": "arubboth, a place in palestine",
    "H786": "arumah, a place in palestine", "H787": "arus", "H788": "a curse", "H789": "arvad, a city-island of palestine", "H790": "an arvadite or citizen of arvad",
    "H791": "ashdowd", "H792": "ashdowdiy", "H793": "fire", "H794": "fire", "H795": "foundation, bottom",
    "H796": "ashdowdiyth", "H797": "ashdoth hap-pisgah, a place east of the jordan", "H798": "ashemah, a heathen deity", "H799": "fire", "H800": "offering by fire",
    "H801": "a fire", "H802": "a woman, wife, female", "H803": "a woman", "H804": "assyria, assyrian", "H805": "ashuriy or ashshuriy, an ashurite or inhabitant...",
    "H806": "ashchur, an israelite", "H807": "ashiyshah", "H808": "a foundation", "H809": "a fire-place", "H810": "to decline",
    "H811": "eshkol, the name of an amorite, also of a val", "H812": "eshkaloniy, an eshkalonite or inhabitant of esh...", "H813": "ashkenaz, a japhethite, also his descendants", "H814": "a testicle", "H815": "eshta'ol, a place in palestine",
    "H816": "to be guilty", "H817": "guilt, fault, sin offering, trespass offering", "H818": "guilty", "H819": "guiltiness, guilt, offence, sin, trespass", "H820": "to grow stout",
    "H821": "an eshtaulite or inhabitant of eshtaol", "H822": "ashphoth", "H823": "ashpenaz, a babylonian", "H824": "ashqar", "H825": "a quiver",
    "H826": "ashur", "H827": "a step", "H828": "ashshur", "H829": "asher, a son of jacob, and the tribe descended ...", "H830": "asherah or the grove",
    "H831": "asheri, an asherite or descendant of asher", "H832": "asherah", "H833": "to be straight, level, right, happy", "H834": "which, who, that which", "H835": "happiness, blessedness",
    "H836": "a grove", "H837": "happy", "H838": "to go straight", "H839": "a step", "H840": "a step",
    "H841": "asare'l, an israelite", "H842": "aserah", "H843": "asri'el, an israelite", "H844": "asri'eliy, an asrielite or descendant of asriel", "H845": "which",
    "H846": "ashar", "H847": "box-tree", "H848": "ashur", "H849": "ashur", "H850": "ashurim",
    "H851": "ashur", "H852": "sign", "H853": "you", "H854": "you", "H855": "you",
    "H856": "you", "H857": "you", "H858": "you", "H859": "you", "H860": "to come near",
    "H861": "athalya", "H862": "athanim", "H863": "athaq", "H864": "ethniy, an israelite", "H865": "hire",
    "H866": "a gift", "H867": "a gift", "H868": "hire", "H869": "ethnan, the name of two israelites", "H870": "athaliah",
    "H871": "athar", "H872": "be'ah", "H873": "bi'ush", "H874": "to search", "H875": "to smell bad, stink",
    "H876": "a well", "H877": "stink", "H878": "to dig", "H879": "to make clear, declare, explain", "H880": "be'erah, an israelite",
    "H881": "stink", "H882": "a well", "H883": "a well", "H884": "be'er sheba`", "H885": "be'er 'elohiym kay",
    "H886": "be'er la-kay ro'iy", "H887": "to have a bad smell", "H888": "a cistern", "H889": "stinking", "H890": "a stink",
    "H891": "be`oshtrah", "H892": "be'eroth", "H893": "be'eroth beney-ya`aqan", "H894": "to boil", "H895": "babel",
    "H896": "babel", "H897": "bebay, an israelite", "H898": "to loathe", "H899": "a testicle", "H900": "bedad, an edomite",
    "H901": "to divide, separate, distinguish, differ", "H902": "separation", "H903": "a part", "H904": "white linen", "H905": "separation, alone, apart, by itself, besides, ...",
    "H906": "alone", "H907": "exclusiveness", "H908": "a liar, lie", "H909": "separation", "H910": "separated",
    "H911": "bedanyah, an israelite", "H912": "bedan, the name of two israelites", "H913": "bdellium", "H914": "to separate, divide, select", "H915": "separated, withdrawal",
    "H916": "tin", "H917": "bedeqar, an israelite", "H918": "to search", "H919": "to search", "H920": "bidqar",
    "H921": "behold!, lo!", "H922": "to be turbid", "H923": "behalah", "H924": "to tremble inwardly", "H925": "pale",
    "H926": "to terrify, hasten, be hasty, be amazed, be af...", "H927": "terrified", "H928": "terror, dismay", "H929": "a dumb beast", "H930": "a beast",
    "H931": "behemoth", "H932": "a thumb, great toe", "H933": "bohen", "H934": "a thumb, great toe", "H935": "to come in, come, go in, go",
    "H936": "destruction", "H937": "boaz, the name of david's great-grandfather an...", "H938": "buz, the name of a son of nahor, and of an isra...", "H939": "buz, the name of a son of nahor, and of an isra...", "H940": "a buziyte or descendant of buz",
    "H941": "contempt", "H942": "bavay, an israelite", "H943": "to trample", "H944": "a treading down", "H945": "a marsh",
    "H946": "contemptuously", "H947": "to despise", "H948": "contemptible", "H949": "despised", "H950": "a despising",
    "H951": "contempt", "H952": "boker", "H953": "to gaze", "H954": "to waste", "H955": "bura'",
    "H956": "bur", "H957": "to bore", "H958": "to make clear", "H959": "to enclose", "H960": "bazah",
    "H961": "booty, prey, spoil", "H962": "to spoil", "H963": "contempt", "H964": "bizyowthyah, a place in palestine", "H965": "to scatter",
    "H966": "bezale'l, the name of two israelites", "H967": "lightning", "H968": "bazluth or bazlith, an israelite", "H969": "biztha', a eunuch of xerxes", "H970": "to select",
    "H971": "to trample down", "H972": "selection", "H973": "examined", "H974": "to test, try", "H975": "a touchstone",
    "H976": "trial", "H977": "to choose", "H978": "choice", "H979": "young man, chosen", "H980": "young women",
    "H981": "choice", "H982": "to trust", "H983": "trust", "H984": "confident", "H985": "security",
    "H986": "trust", "H987": "security", "H988": "to desist from labor", "H989": "vegetable", "H990": "belly, body, womb",
    "H991": "beten, a place in palestine", "H992": "pistachio nut", "H993": "empty", "H994": "to discern, understand, consider", "H995": "to distinguish, understand",
    "H996": "between, among, in the midst of (also adv.), fr...", "H997": "between", "H998": "understanding", "H999": "an interval", "H1000": "a house",
    "H1001": "a fortress", "H1002": "a fortress", "H1003": "a temple", "H1004": "a house", "H1005": "a house",
    "H1006": "bayith, a place in palestine", "H1007": "house of idolatry", "H1008": "house of god", "H1009": "house of arbel", "H1010": "house of the palm-tree",
    "H1011": "house of aven", "H1012": "house of the ashima", "H1013": "house of baal", "H1014": "house of peor", "H1015": "house of baruch",
    "H1016": "house of the fortress", "H1017": "house of the locust", "H1018": "house of acceptance", "H1019": "house of barea", "H1020": "house of the site",
    "H1021": "house of the gazelle", "H1022": "house of bread", "H1023": "house of bread", "H1024": "house of dagon", "H1025": "house of dagon",
    "H1026": "house of diblathaim", "H1027": "house of god", "H1028": "house of gilgal", "H1029": "house of the fortress", "H1030": "house of the gardens",
    "H1031": "house of gamul", "H1032": "house of hakerem", "H1033": "house of the desert", "H1034": "house of charan", "H1035": "house of choron",
    "H1036": "house of yeshimoth", "H1037": "house of lebaoth", "H1038": "house of aphrah", "H1039": "house of bread", "H1040": "house of bread",
    "H1041": "bethuel, the name of a nephew of abraham, and ...", "H1042": "bethuel", "H1043": "bethul, a place in palestine", "H1044": "house of the gap", "H1045": "house of tsur",
    "H1046": "house of zechariah", "H1047": "house of the mark", "H1048": "house of the vineyards", "H1049": "house of hoglah", "H1050": "house of favor",
    "H1051": "house of winter", "H1052": "house of the partridge", "H1053": "house of the lioness", "H1054": "house of maakah", "H1055": "house of marks",
    "H1056": "house of millo", "H1057": "house of millo", "H1058": "house of nimrah", "H1059": "house of distance", "H1060": "house of eden",
    "H1061": "house of oppression", "H1062": "house of peace", "H1063": "house of the breach", "H1064": "house of the rock", "H1065": "house of the boundary",
    "H1066": "house of the acacia", "H1067": "house of the sun", "H1068": "house of the sun", "H1069": "house of anath", "H1070": "house of anoth",
    "H1071": "house of the apple", "H1072": "house of the apple", "H1073": "house of the arabah", "H1074": "house of ashtaroth", "H1075": "house of rekhob",
    "H1076": "a house", "H1077": "outer, external", "H1078": "a girl", "H1079": "a weeping", "H1080": "to weep",
    "H1081": "weeping", "H1082": "to weep", "H1083": "a weeping", "H1084": "bala'", "H1085": "bel'e",
    "H1086": "to swallow down, swallow up, engulf, devour", "H1087": "a swallowing, devouring, destruction", "H1088": "destruction", "H1089": "to wear out, decay, become old", "H1090": "worn out",
    "H1091": "not, except, unless", "H1092": "old rags", "H1093": "failure", "H1094": "old", "H1095": "beliyya`al",
    "H1096": "beliyl", "H1097": "without, not, because not, none", "H1098": "to trouble, wear out, vex", "H1099": "belshatstsar or belshatstsar, belshazzar, a ba...", "H1100": "beli",
    "H1101": "to fall away, fail", "H1102": "to restrain", "H1103": "to mix (specifically grain with oil)", "H1104": "to swallow down, destroy", "H1105": "belshatstsar",
    "H1106": "a son", "H1107": "a building", "H1108": "son of abinadab", "H1109": "biltshan, an israelite", "H1110": "biltiy",
    "H1111": "a platform, scaffold", "H1112": "bilgah or bilgay, the name of two israelites", "H1113": "bilgay", "H1114": "bildad, one of job's friends", "H1115": "without",
    "H1116": "a high place", "H1117": "a high place", "H1118": "bamowth ba'al", "H1119": "a high place", "H1120": "a high place",
    "H1121": "a son", "H1122": "ben", "H1123": "son", "H1124": "son of abiynadab", "H1125": "son of strength",
    "H1126": "son of my people", "H1127": "son of death", "H1128": "son of priecing", "H1129": "ben (a son)", "H1130": "ben (son)", "H1131": "bena (to build)", "H1132": "ben-abyinadab (son of Abinadab)", "H1133": "ben-geher (son of Geber)", "H1134": "ben-deqer (son of Deker)", "H1135": "ben-hur (son of Hur)", "H1136": "ben-hesed (son of Hesed)", "H1137": "ben-hayil (son of strength)", "H1138": "binyan (a building)", "H1139": "ben-hinom (son of Hinnom)", "H1140": "binyah (posterity)", "H1141": "benyamin (Benjamin, son of the right hand)", "H1142": "ben-yemini (a Benjamite)", "H1143": "ben-yishay (son of Jesse)", "H1144": "binyamin (Benjamin)", "H1145": "ben-karmi (son of Carmi)", "H1146": "binnah (building)", "H1147": "bin'a (Binea, a descendant of Saul)", "H1148": "bne (children)", "H1149": "be'esah (a despising)", "H1150": "ben-zoheth (son of Zoheth)", "H1151": "bas (a daughter)", "H1152": "bis'ah (a bog)", "H1153": "betsah (an egg)", "H1154": "bits'on (fortification)", "H1155": "bitsar (an enclosure)", "H1156": "ba'a (to inquire)", "H1157": "ba'ah (a prayer)", "H1158": "ba'ar (to burn)", "H1159": "ba'ah (a petition)", "H1160": "ba'al (to rule)", "H1161": "ba'el (Baal)", "H1162": "bo'el (a possessor)",  "H1163": "ba'al (owner)", "H1164": "ba'al (Baal)", "H1165": "be'el (Beel)", "H1166": "ba'al (to marry)", "H1167": "ba'al (a master)", "H1168": "ba'al (Baal, a god)", "H1169": "ba'al berith (Baal-berith)",  "H1170": "ba'al gad (Baal-gad)", "H1171": "ba'al hamon (Baal-hamon)", "H1172": "ba'alah (mistress)", "H1173": "ba'alath (Baalath)", "H1174": "ba'alath be'er (Baalath-beer)", "H1175": "ba'al zevuv (Baal-zebub)",  "H1176": "ba'al zevul (Baal-zebul)", "H1177": "ba'al hanan (Baal-hanan)", "H1178": "ba'al hatsor (Baal-hazor)", "H1179": "ba'al chermon (Baal-hermon)", "H1180": "ba'ale (lords)", "H1181": "ba'ale yehudah (Baale-Judah)", "H1182": "ba'al me'on (Baal-meon)", "H1183": "ba'al pe'or (Baal-peor)", "H1184": "ba'al peratsim (Baal-perazim)", "H1185": "ba'al tsedeq (lord of righteousness)", "H1186": "ba'al qorban (lord of offering)", "H1187": "ba'al tamar (Baal-tamar)", "H1188": "ba'al zebub (Baal-zebub)", "H1189": "ba'al shalishah (Baal-shalisha)", "H1190": "ba'ar (to be brutish)", "H1191": "ba'alath (Baalath)", "H1192": "ba'alath (Baalath)", "H1193": "ba'ar (brutish)", "H1194": "ba'ash (to stink)", "H1195": "ba'ash (to smell bad)", "H1196": "ba'ash (to stink)", "H1197": "be'osh (stench)", "H1198": "ba'ar (to clear)", "H1199": "ba'ar (to feed on)", "H1200": "be'er (a pit, well)",# --- Batch H1201-H1250 ---
'H1201': 'baash; a primitive root; to smell bad; figuratively, to be offensive morally: - (make to) be abhorred (had in abomination, odious, ) x stank, x utterly.',
'H1202': 'bad; from H909; separation; by implication, a part of the body, branch of a tree, bar for carrying; figuratively, a chief of a city; especially (with prepositional prefix) as an adverb, apart, only, besides: - alone, apart, bar, besides, branch, by self, of each alike, except, only, part, staff, strength.',
'H1203': 'bad; from H909; flaxen thread or yarn; hence, a linen garment: - linen.',
'H1204': 'bada; from H909; (figuratively) a lie: - lie, liar.',
'H1205': 'baat; a primitive root; to trample down: - kick.',
'H1206': 'bats; from H1219 (as feminine of H1202); the mem- bers (pl.) of a person: - (strong) ones.',
'H1207': 'baddim; plural of H1203; white garments: - (white) linen.',
'H1208': 'batsah; a primitive root; to dig for, i.e. pull up by the roots: - pluck up.',
'H1209': 'batsal; probably from a derivative of H1210 (by peeling); an onion (as divided into coats): - onion.',
'H1210': 'batsel; a root probably meaning to peel: - only.',
'H1211': 'batsor; from H1219; inaccessible, i.e. lofty: - vintage.',
'H1212': 'Beetsay; from the same as H1206; domineering; Betsai, the name of two Israelites: - Bezai.',
'H1213': 'batsiyq; from H1216; dough (as swelling by fermentation): - dough.',
'H1214': 'batsa; a primitive root; to break off, i.e. (usually) plunder; (by implication) to finish, or (intransitively) stop: - (be) covet(-ous), cut off, finish, fulfil, gain (greedily), get, be given to (covetousness), greedy, perform, be wounded.',
'H1215': 'betsa; from H1214; plunder; by extension, gain (usually unjust): - covetousness, (dishonest) gain, lucre, profit.',
'H1216': 'batseq; a primitive root; to swell, i.e. swell up, or (by implication) be blistered: - swell.',
'H1217': 'botseq; from H1216 (in the sense of oozing); mud (as infiltrating): - miry place.',
'H1218': 'Botsqath; from H1216; a swell of ground; Botskath, a place in Palestine: - Bozkath, Boskath.',
'H1219': 'batsar; a primitive root; to clip; used only as denominative from H1211, to gather grapes; also to be isolated (i.e. inaccessible) by height or fortification: - cut off, (de-)fenced, fortify, (grape) gather(-er), mighty things, restrain, strong, wall (up), withhold.',
'H1220': 'betser; from H1219; strictly a clipping, i.e. gold (as dug out): - gold, x thing given.',
'H1221': 'betser; from H1219; an enclosure, i.e. fortress: - fenced.',
'H1222': 'betsorah; feminine of H1221; a fortress: - fenced.',
'H1223': 'batsar; from H1219; precious ore (as inaccessible): - (good) gold.',
'H1224': 'batsar; (Aramaic) corresponding to H1219 in the sense of storing up: - lay up.',
'H1225': 'batsoreth; intensive feminine of H1219 (in the sense of restraint); drought: - dearth, drought.',
'H1226': 'Botsrah; feminine of H1221; a fortress, Botsrah, a place in Edom: - Bozrah.',
'H1227': 'Botsrah; the same as H1226; Botsrah, a place in Moab: - Bozrah.',
'H1228': 'bassar; from H1219; a vintage: - vintage.',
'H1229': 'baqa; a primitive root; to cleave; generally, to rend, break, rip or open: - alas, assign, break (in pieces, through, up), burst, cleave, cut, divide, hatch, rend (asunder), rip up, tear, win.',
'H1230': 'baqa; (Aramaic) corresponding to H1229: - break through.',
'H1231': 'baqa; from H1229; to search: - enquire, search.',
'H1232': 'biqa; from H1229; a fissure: - breach, cleft.',
'H1233': 'beqa; from H1229; a section (half) of a shekel, i.e. a beka (a Jewish weight and coin): - bekah, half a shekel.',
'H1234': 'biqah; from H1229; properly, a split, i.e. a wide level valley between mountains: - plain, valley.',
'H1235': 'baqar; a primitive root; properly, to plough, i.e. break forth, i.e. (figuratively) to inspect, admire, care for, consider: - (make) enquire(-y), (make) search, seek out.',
'H1236': 'baqar; (Aramaic) corresponding to H1235: - enquire, make search.',
'H1237': 'biqqar; from H1235; to inspect: - seek.',
'H1238': 'biqqoreth; from H1235; properly, examination, i.e. (by implication) punishment: - animadversion, seek out.',
'H1239': 'baqar; from H1235; beef cattle or an animal of the ox family of either gender (as used for plowing); collectively, a herd: - beeve, bull, bullock, calf, cow, herd, kine, ox.',
'H1240': 'boqer; from H1239; properly, dawn (as the break of day); generally, morning: - (+) day, early, morning, morrow.',
'H1241': 'baqqarah; from H1239; a seeking; - seek.',
'H1242': 'baqash; a primitive root; to search out (by any method; specifically in prayer and worship); by implication, to strive after: - ask, beg, beseech, desire, enquire, get, make inquisition, procure, (make) request, require, seek (for).',
'H1243': 'baqqashah; from H1242; a petition: - request.',
'H1244': 'bar; from H1305 (in the sense of winnowing); grain of any kind (even while standing in the field); by extens. food: - corn, wheat.',
'H1245': 'bar; (Aramaic) corresponding to H1244; a field: - field.',
'H1246': 'bar; from H1305 (in the sense of purity); clear, i.e. (figuratively) clean (morally): - clean, pure.',
'H1247': 'bar; (Aramaic) from a root corresponding to H1305 (in the sense of possessor); a son (as heir); (plural) sons (collectively): - x old, son.',
'H1248': 'bar; borrowed from H1247 (in the sense of attachment); the bosom: - bosom.',
'H1249': 'bar; from H1305; beloved: - son. Compare H1121.',
'H1250': 'bar; or bar; from H1305 (in its original sense); purely: - choice, clean, clear, pure.',
# --- Batch H1251-H1300 ---
'H1251': 'barbur; by reduplication from H1305; a fowl (as fattened): - fowl.',
'H1252': 'barad; a primitive root; to hail: - hail.',
'H1253': 'barad; (Aramaic) from a root corresponding to H1252; hail: - hail.',
'H1254': 'barah; a primitive root; to select; also (as denominative from H1250) to feed; also (as equivalent to H1305) to render clear (color): - choose, declare, eat, x ever, make fat, feed, manifest, (make) plain(-ly), purge, receive, x surely.',
'H1255': 'barod; from H1252 (in the sense of cooling); cold: - cold.',
'H1256': 'berod; from H1252; hail: - hail.',
'H1257': 'barad; from H1252; spotted (as if with hail): - grisled.',
'H1Section_2': 'Barak; from H1300; lightning; Barak, an Israelite: - Barak.',
'H1258': 'barah; from H1254; food: - meat.',
'H1259': 'barak; a primitive root; to kneel; by implication to bless God (as an act of adoration), and (vice-versa) man (as a benefit); also (by euphemism) to curse (God or the king, as treason): - X abundantly, X altogether, X at all, bless, congratulate, curse, X greatly, X indeed, kneel (down), praise, salute, X still, thank.',
'H1260': 'barak; (Aramaic) corresponding to H1259: - bless, kneel.',
'H1261': 'berek; from H1259; a knee: - knee.',
'H1262': 'berek; (Aramaic) corresponding to H1261: - knee.',
'H1263': 'berakah; from H1259; benediction; by implication prosperity: - blessing, liberal, pool, present.',
'H1264': 'Berekah; the same as H1263; Berekah, the name of an Israelite, and also of a valley in Palestine: - Berachah.',
'H1265': 'berekyah; from H1263 and H3050; blessing of Jah; Berebjah, the name of six Israelites: - Berechiah.',
'H1266': 'berekah; feminine from H1259; a reservoir (at which camels kneel as a resting-place): - (fish-)pool.',
'H1267': 'barom; probably from H1254 (in the sense of clarifying); delicately: - with riches.',
'H1268': 'barur; passive participle from H1305; purified: - choice, clean, clear, pure.',
'H1269': 'baruth; from H1254; food: - meat.',
'H1270': 'barzel; perhaps from the root of H1267 (in the sense of cutting); iron (as cutting); by extension, an iron implement: - (ax) head, iron.',
'H1Details': 'barzel; (Aramaic) corresponding to H1270: - iron.',
'H1272': 'Barzillay; from H1270 (in the sense of strength); iron-hearted; Barzillai, the name of three Israelites: - Barzillai.',
'H1273': 'barach; a primitive root; to bolt, i.e. slip away; by implication, to flee suddenly: - chase (away), drive away, fain, flee (away), put to flight, make haste, reach, run away, shoot.',
'H1274': 'bariach; from H1273; a fugitive: - fugitive.',
'H1275': 'bariach; from H1273; a bolt: - bar.',
'H1276': 'Bariach; the same as H1275; Bariach, an Israelite: - Bariah.',
'H1277': 'bariyach; from H1254 (in the sense of eating); fat: - fat(-ted), -ter, fed, plenteous, rank. See also H1004.',
'H1278': 'beriyach; from H1273; a bolt: - bar.',
'H1279': 'beriyach; from H1277; a fatted animal: - fat.',
'H1280': 'beriyth; from H1254 (in the sense of cutting (like H1252)); a compact (because made by passing between pieces of flesh): - covenant, confederacy, confederate, league.',
'H1281': 'Beriyl; by correction from H1279; Beri, an Israelite: - Beri.',
'H1282': 'Beriyth; the same as H1280; Berith, a Shechemite deity: - Berith.',
'H1283': 'beriyiy; from H1254; fat: - fat.',
'H1284': 'beriym; plural of H1259; blessings: - (extraordinary) afflictions (by euphemism).',
'H1285': 'berith; feminine of H1279; soap (as removing dirt): - soap.',
'H1286': 'barak; from H1259; a blessing: - blessing.',
'H1287': 'barkan; from H1300; a thorn (perhaps as burning): - brier.',
'H1288': 'bareqeth; or bareqath; from H1300; a gem (as flashing), perhaps the emerald: - carbuncle.',
'H1289': 'barkath; from H1259; a blessing: - blessing.',
'H1290': 'Barqos; of uncertain derivation; Barkos, one of the Nethinim: - Barkos.',
'H1291': 'Bara; from H1254; declared; Bara, a king of Sodom: - Bera.',
'H1292': 'baraq; corresponding to H1300; lightning: - bright, lightning.',
'H1293': 'Baraqel; from H1290 and H410; God has blessed; Barakel, the father of Elihu: - Barachel.',
'H1294': 'Berakah; from H1259; a blessing: - blessing.',
'H1295': 'barar; a primitive root; to clarify (i.e. brighten), examine, select: - make bright, choice, chosen, cleanse (be clean), clearly, polished, (shew self) pure(-ify), purge (out).',
'H1296': 'Berayay; from H1254 and H3050; Jah has created; Berajah, an Israelite: - Beraiah.',
'H1297': 'barar; (Aramaic) corresponding to H1295: - choice.',
'H1298': 'berar; from H1295; a kernel (as cleared): - corn, wheat.',
'H1299': 'barar; from H1295; pure, clear: - bright, clean, pure.',
'H1300': 'baraq; a primitive root; to lighten (lightning): - cast forth.',# --- Batch H1301-H1400 ---
'H1301': 'baraq; from H1300; lightning; by analogy, a gleam; concretely, a flashing sword: - bright, glitter(-ing sword), lightning.',
'H1302': 'Baraq; from H1301; lightning; Barak, an Israelite: - Barak.',
'H1303': 'baraqan; from H1301; a thorn (perhaps as burning): - brier.',
'H1304': 'bareqeth; or bareqath; from H1301; a gem (as flashing), perhaps the emerald: - carbuncle.',
'H1305': 'barar; a primitive root; to clarify (i.e. brighten), examine, select: - make bright, choice, chosen, cleanse (be clean), clearly, polished, (shew self) pure(-ify), purge (out).',
'H1306': 'Berayay; from H1254 and H3050; Jah has created; Berajah, an Israelite: - Beraiah.',
'H1307': 'barar; (Aramaic) corresponding to H1305: - choice.',
'H1308': 'berar; from H1307; a kernel (as cleared): - corn, wheat.',
'H1309': 'baras; a primitive root; to pierce; by analogy, to bristle as a field of grain: - (be) sharp.',
'H1310': 'basam; from an unused root meaning to be fragrant; spice: - spice.',
'H1311': 'besem; from H1310; fragrance; by implication, spicery: - spice, sweet (odour).',
'H1312': 'bosem; from H1310; spice: - spice, sweet.',
'H1313': 'basam; or basom; from H1310; the balsam plant: - spice.',
'H1314': 'Bosmath; feminine of H1313 (in the sense of H1311); fragrance; Bosmath, the name of a wife of Esau, and of a daughter of Solomon: - Bashemath, Basmath.',
'H1315': 'bashal; a primitive root; to boil; specifically, to be done in cooking; figuratively, to ripen: - bake, boil, bring forth, roast, seethe, sod (pottage).',
'H1316': 'bashel; from H1315; boiled: - sodden.',
'H1317': 'bashal; (Aramaic) corresponding to H1315: - be sodden.',
'H1318': 'bashan; of uncertain derivation; Bashan (often with the article), a region East of the Jordan: - Bashan.',
'H1319': 'basar; a primitive root; to be fresh, i.e. full (rosy, (figuratively) cheerful); to announce (glad news): - messenger, preach, publish, shew forth, (bear, bring, carry, preach, good, tell good) tidings.',
'H1320': 'basar; from H1319; flesh (from its freshness); by extension, body, person; also (by euphemism) the pudenda of a man: - body, fat(-fleshed), lean(-fleshed), lust, man, mankind, + nakedness, self, skin.',
'H1321': 'basar; (Aramaic) corresponding to H1320: - flesh.',
'H1322': 'besorah; feminine of H1320; glad news: - reward for tidings.',
'H1323': 'bashash; a primitive root; to be ashamed (via the idea of shrinking from publicity): - be ashamed, confounded, delayed.',
'H1324': 'bath; from H1197 (as feminine); a house: - daughter. See H1121.',
'H1325': 'bath; from H1197 (in the sense of H1129); a bath (a Jewish measure of liquids): - bath.',
'H1326': 'bath; (Aramaic) corresponding to H1325: - bath.',
'H1327': 'batta; of uncertain derivation; a precipice: - desolate.',
'H1328': 'batah; from H982; a trust: - confidence.',
'H1329': 'bathah; or battah; from an unused root perhaps meaning to break in pieces; desolation: - waste.',
'H1330': 'bathach; a primitive root; properly, to hie for refuge; figuratively, to trust, be confident or sure: - be bold (confident, secure, sure), careless (one, woman), put confidence, (make to) hope, (put) trust.',
'H1331': 'betach; from H1330; properly, a place of refuge; abstractly, safety, both objective (security) and subjective (confidence): - assurance, care(-less), confidence, hope, safe(-ly, -ty), secure, surely.',
'H1332': 'butechah; from H1330; confidence: - confidence.',
'H1333': 'bitchah; feminine of H1331; trust: - confidence, trust.',
'H1334': 'batchown; from H1330; trust: - confidence.',
'H1335': 'bittachown; from H1330; trust: - confidence, hope.',
'H1336': 'batal; a primitive root; to desist from labor: - cease.',
'H1337': 'batal; (Aramaic) corresponding to H1336; to cease: - (make to) cease, fail, let (respite from) work.',
'H1338': 'betel; from H1337; cessation: - void.',
'H1339': 'baten; from an unused root probably meaning to be hollow; the belly, especially the womb; also the bosom: - belly, body, + within, womb.',
'H1Video': 'beten; from H1339; the belly: - belly.',
'H1341': 'beten; (Aramaic) from a root corresponding to H1339; the belly: - belly.',
'H1342': 'boten; from H1339; the pistacia-nut (from its form): - nut.',
'H1343': 'biththah; of uncertain derivation; a palace: - palace.',
'H1344': 'gaah; a primitive root; to mount up; hence, to be majestic: - gloriously, grow up, increase, be risen, triumph.',
'H1345': 'gaah; from H1344; arrogance: - pride.',
'H1346': 'gaavah; from H1344; arrogance or majesty; by implication, (concretely) ornament: - excellency, haughtiness, highness, pride, swelling.',
'H1Details': 'gaayon; from H1344; the same as H1345: - arrogance, excellency(-lence), majesty, pomp, pride, swelling.',
'H1348': 'geuth; from H1344; majesty, i.e. (figuratively) pride: - highness, majesty, pride, swelling.',
'H1349': 'gev; from H1344 (in the sense of H1461); the back, i.e. (by extension) the person: - back, body.',
'H1350': 'gaal; a primitive root, to redeem (according to the Oriental law of kinship), i.e. to be the next of kin (and as such to buy back a relatives property, marry his widow, etc.): - X in any wise, X at all, avenger, deliver, (do, perform the part of near, next) kinsfolk(-man), purchase, ransom, redeem(-er), revenger.',
'H1351': 'gaal; a primitive root; to soil or (figuratively) desecrate: - defile, pollute, stain.',
'H1352': 'gaal; a primitive root; to loathe: - abhor, fail.',
'H1353': 'goel; from H1351; profanation: - profane.',
'H1354': 'gab; from an unused root meaning to hollow or curve; the back (as rounded), outside: - back, boss, brow, eyebrow, hollow(-ness), + out(side), ring, upon.',
'H1355': 'gab; (Aramaic) corresponding to H1354: - back.',
'H1356': 'geb; from H1461; a locust (as arching the back), a cistern (as vaulted): - pit, + swarm of locusts.',
'H1357': 'geb; (Aramaic) from a root corresponding to H1356; a pit: - den.',
'H1358': 'gob; from H1461; a locust (as an archer): - locust.','Video': 'gob; from H1461; a locust (as an archer): - locust.',
'H1359': 'Gob; from H1358; Gob, a place in Palestine: - Gob.',
'H1360': 'gobah; from H1364; height: - height, high.',
'H1361': 'gabahh; a primitive root; to be lofty (literally or figuratively): - be (+ exalted), height, (be, lift up, mount up, be on) high(-er), lofty, proud, X very.',
'H1362': 'gabahh; from H1361; lofty (in condition or bearing): - high, proud.',
'H1363': 'gobahh; from H1361; elation, grandeur, arrogance: - excellency, haughty, height, high, loftiness, pride.',
'H1364': 'gabeha; from H1361; lofty: - high.',
'H1365': 'gabhuth; from H1361; pride: - loftiness, lofty.',
'H1Body': 'gabach; from H1361; a bald forehead: - bald forehead.',
'H1367': 'gabbachath; from H1366; baldness in the forehead: - bald head, + without hair.',
'H1368': 'gibbor; or gibbor; intensive from the same as H1397; powerful; by implication, warrior, tyrant: - champion, chief, X excel, giant, man, mighty (man, one), strong (man), valiant man.',
'H1369': 'geburah; feminine from H1368; force (literally or figuratively); by implication, valor, victory: - force, mastery, might, mighty (act, power), power, strength.',
'H1370': 'geburah; (Aramaic) corresponding to H1369: - might.',
'H1371': 'gibbar; (Aramaic) corresponding to H1368: - mighty.',
'H1372': 'gibbem; a variation of H1367: - bald head.',
'H1373': 'gibben; from H1372; humped (as a camel): - crookbackt.',
'H1374': 'Gabben; from H1372; Gabben, a place in Palestine: - Gibbethon.',
'H1375': 'gebiyl; from H1378; a cup: - cup.',
'H1376': 'gebiya; from an unused root (meaning to be convex); a goblet; by analogy, the calyx of a flower: - cup, pot.',
'H1377': 'gebiyr; from H1396; a master: - lord.',
'H1378': 'Gebiyr; from H1396; Gebir, an Israelite: - Geber.',
'H1379': 'gebiyrah; feminine of H1377; a mistress, i.e. queen: - queen.',
'H1380': 'gabal; a primitive root; properly, to twist as a rope; only as denominative from H1384, to bound, i.e. border: - set bounds, border.',
'H1381': 'gebal; from H1380; a boundary, i.e. (by implication) a region: - border, bound, coast, landmark, limit, space, spot.',
'H1382': 'gebal; (Aramaic) corresponding to H1381: - bound.',
'H1383': 'gabluth; from H1380; a twisting, i.e. (concretely) a border: - end.',
'H1384': 'Gebal; from H1380 (in the sense of enclosing); a mountain; Gebal, a place in Phoenicia: - Gebal.',
'H1385': 'giblah; from H1380; a boundary: - border.',
'H1386': 'Gibliy; patrial from H1384; a Gebalite, or inhabitant of Gebal: - Giblite, stone-squarer.',
'H1387': 'gablul; from an unused root (meaning to roll); a cake (as rolled): - cake.',
'H1388': 'geban; (Aramaic) from a root corresponding to H1389; cheese: - cheese.',
'H1389': 'gaben; from an unused root probably meaning to be arched or contracted; a hillock: - high place.',
'H1390': 'gibnah; feminine from H1389; cheese (as curdled): - cheese.',
'H1391': 'Gabai; from H1354 (in the sense of tax); a collector; Gabbai, an Israelite: - Gabbai.',
'H1392': 'gibboen; from H1389; hilly; Gibon, a place in Palestine, with a stream and pool: - Gibeon.',
'H1393': 'Giboniy; patrial from H1392; a Gibonite: - Gibeonite.',
'H1Sure': 'gibol; from H1380; a boundary: - border.',
'H1395': 'Gibath; from H1389; a hillock; Gibath, a place in Palestine: - Gibeah.',
'H1396': 'gabar; a primitive root; to be strong; by implication, to conquer, act insolently: - exceed, confirm, be great, be mighty(-ier), prevail, strengthen, be strong, be valiant.',
'H1397': 'geber; from H1396; properly, a valiant man or warrior; generally, a person simply: - every one, man, + mighty.',
'H1398': 'gebar; (Aramaic) from a root corresponding to H1396; a man: - man.',
'H1399': 'Gaber; from H1396; valiant; Geber, the name of two Israelites: - Geber.',
'H1400': 'gebar; from H1396; a man: - man.',
# --- Batch H1401-H1500 ---
'H1401': 'Gabriy\'el; from H1397 and H410; man of God; Gabriel, an archangel: - Gabriel.',
'H1402': 'gabriy; from H1397; a man: - man.',
'H1403': 'Gibriy; from H1397; manly; Gibri, an Israelite: - Gibri.',
'H1404': 'gabruth; from H1397; mastery: - strength.',
'H1405': 'Geba; from H1389; a hill; Geba, a place in Palestine: - Gaba, Geba, Gibeah.',
'H1406': 'Gibea; from H1389; a hillock; Gibea, a place in Palestine: - Gibeah.',
'H1407': 'Gibea; the same as H1406; Gibea, an Israelite: - Gibea.',
'H1408': 'Gibeath; from H1389; a hillock; Gibeath, a place in Palestine: - Gibeath.',
'H1409': 'Gibon; from H1389; hilly; Gibon, a place in Palestine, with a stream and pool: - Gibeon.',
'H1410': 'Giboniy; patrial from H1409; a Gibonite: - Gibeonite.',
'H1411': 'gibol; from H1380; a boundary: - border.',
'H1412': 'Gibath; from H1389; a hillock; Gibath, a place in Palestine: - Gibeah.',
'H1413': 'gad; from H1464 (in the sense of cutting); coriander seed (from its furrows): - coriander.',
'H1414': 'Gad; from H1464; Gad, a son of Jacob, including his tribe and its territory; also a prophet: - Gad.',
'H1415': 'Gad; a variation of H1414; Gad, a prophet: - Gad.',
'H1416': 'gad; from H1464 (in the sense of distributing); fortune: - troop.',
'H1417': 'gada; a primitive root; to fell a tree; generally, to destroy anything: - cut (asunder, in sunder, down, off), hew down.',
'H1418': 'gidda; (Aramaic) from H1417; to cut: - hew down.',
'H1419': 'gadowl; or (shortened) gadol; from H1431; great (in any sense); hence, older; also insolent: - + aloud, elder(-est), + exceeding(-ly), + far, great(-er, -ly, -ness), high, long, loud, mighty, more, much, noble, proud, + sore, X very.',
'H1420': 'geduwlah; or (shortened) gedullah; feminine of H1419; greatness; (concretely) a great deed, or (abstractly) dignity: - great things(-ness), majesty.',
'H1421': 'geduwlah; (Aramaic) corresponding to H1420: - greatness.',
'H1422': 'gadiy; from H1416 (in the sense of H1424); a kid: - kid.',
'H1423': 'gidduwph; or gidduph; and (feminine) gidduphah; from H1441; defamation: - blasphemy, reproach, taunt.',
'H1424': 'gediy; from the same as H1413; a kid (from its rapid motion); as feminine, a young goat; figuratively, a rosette (as a pet): - (she) goat, kid.',
'H1425': 'gediyah; feminine of H1424; a young goat: - kid.',
'H1426': 'gadiysh; from an unused root (meaning to heap up); a stack of sheaves, i.e. a tomb: - shock (of corn), stack, tomb.',
'H1427': 'Gadiy; from H1414; fortunate; Gadi, an Israelite: - Gadi.',
'H1428': 'Gaddiy; from H1414; fortunate; Gaddi, an Israelite: - Gaddi.',
'H1429': 'Gaddiy\'el; from H1414 and H410; fortune of God; Gaddiel, an Israelite: - Gaddiel.',
'H1430': 'gadal; a primitive root; to twist (comp. H1434), i.e. to be (causatively make) large (in various senses, as in body, mind, estate or honor, also in pride): - advance, boast, bring up, exceed, excellent, be(-come, do, get, make, wax) great(-er, -ly, -ness), grow(up), heap, increase, loud, magnify(-ical), be much set by, nourish (up), pass, promote, proudly (spoken), tower.',
'H1431': 'gadel; from H1430; large (literally or figuratively): - great, grew.',
'H1432': 'gadel; from H1430; large (in body or estate); adverbially, greatly: - great, wealthy.',
'H1433': 'godel; from H1430; greatness (literally or figuratively): - dignity, great(-ness), majesty, pride, stoutness.',
'H1434': 'gedil; from H1430 (in the sense of twisting); thread, i.e. a tassel or festoon: - fringe, wreath.',
'H1435': 'Giddal; from H1430; Giddal, one of the Nethinim: - Gidal.',
'H1436': 'Giddel; from H1430; stout; Giddel, the name of two Nethinim: - Giddel.',
'H1437': 'Gidom; from H1430; a cutting (i.e. desolation); Gidom, a place in Palestine: - Gidom',
'H1438': 'gada; a primitive root; to cut off or down: - cut asunder (down), hew down.',
'H1439': 'Gidon; from H1438; a feller (i.e. warrior); Gidon, an Israelite: - Gideon.',
'H1440': 'Gidoniy; from H1439; a Gidonite (if correct; rather a patronymic from Gidon): - Gideoni.',
'H1441': 'gadaph; a primitive root; to hack (with words), i.e. revile, blaspheme: - blaspheme, reproach.',
'H1442': 'gadaph; (Aramaic) corresponding to H1441: - blaspheme.',
'H1443': 'gadar; a primitive root; to wall in or around: - close up, fence up, hedge, inclose, make(-r) (up a wall), mason, repairer.',
'H1444': 'geder; from H1443; a circumvallation; by implication, an inclosure: - fence, hedge, wall.',
'H1445': 'Geder; the same as H1444; Geder, a place in Palestine: - Geder.',
'H1446': 'Gedor; from H1443; inclosure; Gedor, a place in Palestine; also the name of two Israelites: - Gedor.',
'H1447': 'gederah; feminine of H1444; an inclosure: - fence, fold, hedge, wall.',
'H1448': 'gederiy; patrial from H1446; a Gederite (or Gedorite): - Gederite.',
'H1449': 'Gederoth; plural of H1447; inclosures; Gederoth, a place in Palestine: - Gederoth.',
'H1450': 'Gederothayim; dual of H1447; two enclosures; Gederothajim, a place in Palestine: - Gederothaim.',
'H1451': 'gah; from H1461; the back: - back.',
'H1452': 'gahah; a primitive root; to remove: - cure.',
'H1453': 'gehah; from H1452; a cure: - medicine.',
'H1454': 'gahar; a primitive root; to prostrate onesf: - cast self down, stretch self.',
'H1455': 'gav; from H1461; the back: - back.',
'H1456': 'gav; from H1461; the middle: - X among, X between, circle, X from, X in, midst, X out of, X through, X within.',
'H1457': 'gav; (Aramaic) corresponding to H1456: - midst.',
'H1458': 'gevah; from H1461; the back, i.e. (by extens.) the person: - body.',
'H1459': 'gevah; feminine of H1458; the back: - back.',
'H1460': 'gevah; from H1461; pride: - pride.',
'H1461': 'gavah; a primitive root; to be convex (as a vault or dome): - lift up.',
'H1462': 'gevah; from H1461; exaltation: - lifting up.',
'H1463': 'govay; from H1461; a locust (as arching the back): - locust.',
'H1464': 'guwd; a primitive root (akin to H1413); to crowd upon, i.e. attack: - invade, overcome.',
'H1465': 'guwd; a primitive root (akin to H1413); to crowd; by implication, to gash (as if by pressing into): - cut.',
'H1466': 'Gudgod; by reduplication from H1465; Gudgod, a place in the Desert: - Gudgodah.',
'H1467': 'gevah; feminine of H1458; the body (as curved): - body.',
'H1468': 'guwz; a primitive root; properly, to shear off; but used only in the (figuratively) sense of passing rapidly: - bring, cut off.',
'H1469': 'guwz; (Aramaic) from a root corresponding to H1468; to pass over: - pass over.',
'H1470': 'Gowzan; of uncertain derivation; Gozan, a province of Assyria: - Gozan.',
'H1471': 'goy; apparently a primary word; a foreign nation; hence, a Gentile; also (figuratively) a troop of animals, or a flight of locusts: - Gentile, heathen, nation, people.',
'H1472': 'geviyah; feminine of H1465; a body, whether alive or dead: - (dead) body, carcase, corpse.',
'H1473': 'guwl; a primitive root; to revolve (in a circle or orbit); by implication, to rejoice: - be glad, joy, be joyful, rejoice.',
'H1474': 'Guwniy; from an unused root meaning to protect; Gunite (collectively) or descendants of Guni: - Gunites.',
'H1Example': 'guwa; from H1461; the back: - back.',
'H1476': 'gava; a primitive root; to expire (breathe out): - be dead, die, give up the ghost, perish.',
'H1477': 'guwph; from an unused root meaning to hollow; a corpse (as the hollow still): - body.',
'H1478': 'guwphah; (Aramaic) feminine of H1477; a corpse: - body.',
'H1479': 'guwr; a primitive root; properly, to turn aside from the road (for a lodging or any other purpose), i.e. sojourn (as a guest); also to shrink, fear (as in avoiding peril); also to gather for hostility (as afraid): - abide, assemble, be afraid, dwell, fear, gather (together), inhabitant, remain, sojourn, stand in awe, stranger, X surely.',
'H1480': 'guwr; (Aramaic) corresponding to H1479: - dwell.',
'H1481': 'guwr; or (shortened) gur; from H1479; a cub (as still abiding in the lair), especially of the lion: - whelp, young (one).',
'H1482': 'Guwr; the same as H1481; Gur, a place in Palestine: - Gur.',
'H1483': 'Guwr-baal; from H1481 and H1168; dwelling of Baal; Gur-baal, a place in Arabia: - Gur-baal.',
'H1484': 'gowral; or (shortened) goral; from an unused root meaning to be rough (as stone); properly, a pebble, i.e. a lot (small stones being used for that purpose); figuratively, a portion or destiny (as if determined by lot): - lot.',
'H1485': 'gavash; from an unused root meaning to collect; a lump: - clod.',
'H1486': 'gazar; a primitive root; to cut down or off; (figuratively) to destroy, divide, exclude, or decide: - cut (down, off), decree, divide, snatch.',
'H1487': 'gazar; (Aramaic) corresponding to H1486: - soothsayer.',
'H1488': 'gezer; from H1486; a portion (as cut off); also a desert (as separated): - part, piece.',
'H1489': 'Gezer; from H1486; a precipice; Gezer, a place in Palestine: - Gazer, Gezer.',
'H1490': 'gizrah; feminine of H1488; the figure or person (as if cut out); also an inclosure (as separated): - polishing, separate place.',
'H1491': 'gizrath; feminine of H1488; a cutting (in the sense of H1486), i.e. a decree: - decree.',
'H1492': 'gazaz; a primitive root (akin to H1468); to cut off; specifically, to shear sheep: - cut off, (sheep-)shearer, shave.',
'H1493': 'gazal; a primitive root; to pluck off; specifically, to flay, strip or rob: - catch, consume, exercise robbery, pluck (off), rob, spoil, take (by violence, away).',
'H1494': 'gazel; from H1493; plunder, i.e. violence: - robbery, violence.',
'H1495': 'gazel; from H1493; robbery, or (concretely) plunder: - that which he took violently away, spoil.',
'H1496': 'gazam; a primitive root; to cut off: - palmer-worm.',
'H1497': 'gazah; from an unused root meaning to cut off; a fleece (as shorn): - fleece.',
'H1498': 'Gazzam; from H1496; devourer; Gazzam, one of the Nethinim: - Gazzam.',
'H1499': 'geza; from an unused root meaning to cut down; the trunk or stump of a tree (as felled or planted): - stem, stock.',
'H1500': 'Gizriy; (with the article) patrial from H1489; a Gizrite (collectively) or inhabitants of Gezer; but better (as in the text) by transposition Girziy; patrial from H1511; a Girzite (collectively) or inhabitants of Gerizim: - Gezrites.',# --- Batch H1501-H1600 (Simple Format) ---
'H1501': 'Gizriy (ghiz-ree)',
'H1502': 'gachown (gaw-khone)',
'H1503': 'gachal (gaw-khal)',
'H1504': 'gacheleth (gah-kheh-leth)',
'H1505': 'Gacham (gah-kham)',
'H1506': 'Gachar (gah-khar)',
'H1507': 'giyach (ghee-akh)',
'H1508': 'giyach (ghee-akh)',
'H1509': 'Giychoq (ghee-khoke)',
'H1510': 'Gichown (ghee-khone)',
'H1511': 'gay gahee',
'H1512': 'giyd (gheed)',
'H1513': 'giyd (gheed)',
'H1514': 'gayt (gaheet)',
'H1515': 'giyl (gheel)',
'H1516': 'giyl (gheel)',
'H1517': 'giyl (gheel)',
'H1518': 'giylah (ghee-law)',
'H1519': 'Giynath (ghee-nath)',
'H1520': 'Giychown (gee-khone)',
'H1521': 'geyr (gare)',
'H1522': 'geyr (gare)',
'H1523': 'giyl (gheel)',
'H1524': 'giyl (gheel)',
'H1525': 'giyl (gheel)',
'H1526': 'Giyloh (ghee-lo)',
'H1527': 'Giyloniy (ghee-lo-nee)',
'H1528': 'gach (gakh)',
'H1529': 'gal (gal)',
'H1530': 'gal (gal)',
'H1531': 'gull (gool)',
'H1532': 'gal (gawl)',
'H1533': 'gil (gheel)',
'H1534': 'gil (gheel)',
'H1535': 'Galed galade',
'H1536': 'gillul (ghil-lool)',
'H1537': 'Gulgoleth (gul-go-leth)',
'H1538': 'gulgoleth (gul-go-leth)',
'H1539': 'galab (gaw-lab)',
'H1540': 'galab (gaw-lawb)',
'H1541': 'galach (gaw-lakh)',
'H1542': 'gallach (gal-lawkh)',
'H1543': 'gilayown (ghil-law-yone)',
'H1544': 'Galiyl (gaw-leel)',
'H1545': 'galiyl (gaw-leel)',
'H1546': 'Geliylah (ghel-ee-law)',
'H1547': 'geliyluth (ghel-ee-looth)',
'H1548': 'gallab (gal-lawb)',
'H1549': 'galam (gaw-lam)',
'H1550': 'gelem (gheh-lem)',
'H1551': 'golem (go-lem)',
'H1552': 'Galal (gaw-lawl)',
'H1Note': 'galal (gaw-lawl)',
'H1554': 'gallal (gal-lawl)',
'H1555': 'gilgal (ghil-gawl)',
'H1556': 'galal (gaw-lal)',
'H1557': 'gelal (ghel-awl)',
'H1558': 'galal (gaw-lawl)',
'H1559': 'Gilalay (ghil-al-ahee',
'H1560': 'galmuwd (gal-mood)',
'H1561': 'gela (gheh-leh)',
'H1562': 'gala (gaw-law)',
'H1563': 'galah (gaw-law)',
'H1564': 'goleh (go-leh)',
'H1565': 'gallach (gal-lawkh)',
'H1566': 'Golyath (gol-yath)',
'H1567': 'Gilyon (ghil-yone)',
'H1568': 'Giloh (ghee-lo)',
'H1569': 'Gilgal (ghil-gawl)',
'H1570': 'galash (gaw-lash)',
'H1571': 'gam (gam)',
'H1572': 'gome (go-meh)',
'H1573': 'gimad (gim-mawd)',
'H1574': 'Gammad (gam-mawd)',
'H1575': 'Gamuwl (gaw-mool)',
'H1576': 'gemuwl (ghem-ool)',
'H1577': 'gemuwlah (ghem-oo-law)',
'H1578': 'gamal (gaw-mal)',
'H1579': 'gamal (gaw-mawl)',
'H1580': 'gamal (gaw-mawl)',
'H1581': 'Gamal (gaw-mawl)',
'H1582': 'Gemalliy (ghem-al-lee)',
'H1583': 'Gimzo (ghim-zo)',
'H1584': 'gamar (gaw-mar)',
'H1485': 'gemar ghemar',
'H1586': 'gamar (gaw-mar)',
'H1587': 'Gemarya (ghem-ar-yaw)',
'H1588': 'Gemaryahu (ghem-ar-yaw-hoo)',
'H1589': 'ganab (gaw-nab)',
'H1590': 'genebah (ghen-ay-baw)',
'H1591': 'gannab (gan-nawb)',
'H1592': 'ganab (gaw-nab)',
'H1593': 'gan (gan)',
'H1594': 'gannah (gan-naw)',
'H1595': 'genez (gheh-nez)',
'H1596': 'genaz (ghen-az)',
'H1597': 'ginzar (ghin-zar)',
'H1598': 'gaac (gaw-as)',
'H1599': 'gaah (gaw-aw)',
'H1600': 'gaal (gaw-al)',
# --- Batch H1601-H1800 (Simple Format) ---
'H1601': 'gaash (gaw-ash)',
'H1602': 'gaal (gaw-al)',
'H1603': 'goal (goal)',
'H1604': 'gaam (gaw-am)',
'H1605': 'gaar (gaw-ar)',
'H1606': 'gearah (gheh-aw-raw)',
'H1607': 'gaash (gaw-ash)',
'H1608': 'Goath (go-ath)',
'H1609': 'gab (gab)',
'H1610': 'gob (gobe)',
'H1611': 'Geb (gabe)',
'H1612': 'gibeach (ghib-ay-akh)',
'H1613': 'gabiya' 'ghebeeah',
'H1614': 'gabiyr (gheb-eer)',
'H1615': 'gebiyrah (gheb-ee-raw)',
'H1616': 'gabish (gaw-beesh)',
'H1617': 'gebiynah (gheb-ee-naw)',
'H1618': 'gabla' 'gablaw',
'H1619': 'gabluth (gab-looth)',
'H1620': 'Giblim (ghib-leem)',
'H1621': 'gabnon (gab-nohn)',
'H1622': 'gaba' 'gaw-bah',
'H1623': 'garab (gaw-rawb)',
'H1624': 'garab (gaw-rawb)',
'H1625': 'gerb (gheh-reb)',
'H1626': 'Gareb (gaw-rabe)',
'H1627': 'gargrowth (gar-gher-owth)',
'H1628': 'gargar (gar-gar)',
'H1629': 'gergerah (gher-gheh-raw)',
'H1630': 'gir (gheer)',
'H1631': 'ger (gare)',
'H1632': 'ger (gare)',
'H1633': 'garad (gaw-rad)',
'H1634': 'garah (gaw-raw)',
'H1635': 'garah (gaw-raw)',
'H1636': 'gerah (gay-raw)',
'H1637': 'garown (gaw-rone)',
'H1638': 'garaz (gaw-raz)',
'H1639': 'garzen (gar-zen)',
'H1640': 'gariyz (gaw-reez)',
'H1641': 'goral (go-rawl)',
'H1642': 'gerem (gheh-rem)',
'H1643': 'gerem (gheh-rem)',
'H1644': 'garam (gaw-ram)',
'H1645': 'gerem (gheh-rem)',
'H1646': 'goren (go-ren)',
'H1647': 'garas (gaw-ras)',
'H1648': 'garaph (gaw-raf)',
'H1649': 'gereph (gheh-ref)',
'H1650': 'garar (gaw-rar)',
'H1651': 'gerar (gher-awr)',
'H1652': 'Gerar (gher-awr)',
'H1653': 'garas (gaw-ras)',
'H1654': 'geres (gheh-res)',
'H1655': 'gariyn (gar-een)',
'H1656': 'gara' 'gawrah',
'H1657': 'Gera' 'gayraw',
'H1658': 'garam (gaw-ram)',
'H1659': 'gara'' (gaw-rah)',
'H1660': 'garia (gaw-ree-ah)',
'H1661': 'gerown (gayr-ohn)',
'H1662': 'Grizim (gher-ee-zeem)',
'H1663': 'Girziy (ghir-zee)',
'H1664': 'gath (gath)',
'H1665': 'geshem (gheh-shem)',
'H1666': 'geshem (gheh-shem)',
'H1667': 'Geshem (gheh-shem)',
'H1668': 'Geshem (gheh-shem)',
'H1669': 'gasham (gaw-sham)',
'H1670': 'geshem (gheh-shem)',
'H1671': 'Geshur (ghesh-oor)',
'H1672': 'Geshuriy (ghesh-oo-ree)',
'H1673': 'gashash (gaw-shash)',
'H1674': 'gath (gath)',
'H1675': 'Gath (gath)',
'H1676': 'Gittiy (ghit-tee)',
'H1677': 'Gittayim (ghit-tah-yim)',
'H1678': 'Gath-Rimmown (gath-rim-mone)',
'H1679': 'Gath-hepher (gath-heh-fer)',
'H1680': 'da (dah)',
'H1681': 'daba',
'H1682': 'dibbah (dib-baw)',
'H1683': 'deba' 'debaw',
'H1684': 'dob' 'dobe',
'H1685': 'dobe' 'do-beh',
'H1686': 'dabaq (daw-bak)',
'H1687': 'debaq (deb-ak)',
'H1688': 'dabaq (daw-bawk)',
'H1689': 'debeq (deh-bek)',
'H1690': 'dabeq (daw-bake)',
'H1691': 'dabar (daw-bar)',
'H1692': 'dabar (daw-bar)',
'H1693': 'dabar (daw-bar)',
'H1694': 'deber (deh-ber)',
'H1695': 'dibber (dib-bare)',
'H1696': 'dabar (daw-bawr)',
'H1697': 'dabar (daw-bawr)',
'H1698': 'dibrah (dib-raw)',
'H1699': 'dobher (do-ber)',
'H1700': 'doberah (dob-er-aw)',
'H1701': 'dabbar (dab-bawr)',
'H1702': 'Dibrayim (dib-rah-yim)',
'H1703': 'dabar (daw-bawr)',
'H1704': 'Dibown (dee-bone)',
'H1705': 'Dibon (dee-bone)',
'H1706': 'Debowrah (deb-o-raw)',
'H1707': 'debiyr (deb-eer)',
'H1Table': 'Debiyr (deb-eer)',
'H1709': 'dabbesheth (dab-beh-sheth)',
'H1710': 'debash (deb-ash)',
'H1711': 'dag (dawg)',
'H1712': 'dagah (daw-gaw)',
'H1713': 'dagah (daw-gaw)',
'H1714': 'Dagown (daw-gone)',
'H1715': 'dagan (daw-gawn)',
'H1716': 'dagar (daw-gar)',
'H1717': 'dagal (daw-gal)',
'H1718': 'degel (deh-ghel)',
'H1719': 'dad (dad)',
'H1720': 'dud (dood)',
'H1721': 'dadah (daw-daw)',
'H1722': 'dod (dode)',
'H1723': 'dowd (dode)',
'H1724': 'duday (doo-dah-ee)',
'H1725': 'dava (daw-vaw)',
'H1726': 'David (daw-veed)',
'H1727': 'David (daw-veed)',
'H1728': 'davvag (dav-vawg)',
'H1729': 'duwg (doog)',
'H1730': 'dowd (dode)',
'H1731': 'dowdah (do-daw)',
'H1732': 'David (daw-veed)',
'H1733': 'Dowdow (do-do)',
'H1734': 'Dowday (do-dah-ee)',
'H1735': 'Dowdavahu (do-daw-vaw-hoo)',
'H1736': 'duwach (doo-akh)',
'H1737': 'duwch (dookh)',
'H1738': 'duchiyphath (doo-khee-fath)',
'H1739': 'davah (daw-vaw)',
'H1740': 'davah (daw-veh)',
'H1741': 'davah (daw-veh)',
'H1742': 'duway (dev-ah-ee)',
'H1743': 'devach (dev-akh)',
'H1744': 'davaq (daw-vak)',
'H1Details': 'davvaq (dav-vawk)',
'H1746': 'duwr (door)',
'H1747': 'duwr (door)',
'H1748': 'duwr (door)',
'H1749': 'duwra (doo-raw)',
'H1750': 'duwsh (doosh)',
'H1751': 'duwsh (doosh)',
'H1752': 'duwsh (doosh)',
'H1753': 'dahab (dah-hab)',
'H1754': 'dehab (deh-hab)',
'H1755': 'dahar (daw-har)',
'H1756': 'daharah (dah-har-aw)',
'H1757': 'duwm (doom)',
'H1758': 'duwmam (doo-mawm)',
'H1759': 'duwmah (doo-maw)',
'H1760': 'duwmiyah (doo-me-yaw)',
'H1761': 'Duwmah (doo-maw)',
'H1762': 'Downag (do-nagh)',
'H1763': 'dachah (daw-khaw)',
'H1764': 'dachah (daw-khaw)',
'H1765': 'dacheh (daw-kheh)',
'H1Two': 'dechiy (dekh-ee)',
'H1767': 'diy (dee)',
'H1768': 'diy (dee)',
'H1769': 'day (dahee)',
'H1770': 'day (dahee)',
'H1771': 'daab (dawab)',
'H1772': 'deabah (deh-aw-baw)',
'H1773': 'deabown (deh-aw-bone)',
'H1774': 'Dag (daw-ag)',
'H1775': 'deagah (deh-aw-gaw)',
'H1776': 'daah (daw-aw)',
'H1777': 'daah (daw-aw)',
'H1778': 'diyg (deeg)',
'H1779': 'duwg (doog)',
'H1780': 'dayag (dah-yawg)',
'H1781': 'dayag (dah-yawg)',
'H1782': 'diyn (deen)',
'H1783': 'diyn (deen)',
'H1784': 'diyn (deen)',
'H1785': 'dayan (dah-yawn)',
'H1786': 'dayan (dah-yawn)',
'H1787': 'dayan (dah-yawn)',
'H1788': 'diynah (dee-naw)',
'H1789': 'Diynah (dee-naw)',
'H1790': 'daya (dah-yaw)',
'H1791': 'deya' 'day-yaw',
'H1792': 'dak (dak)',
'H1793': 'dakka' 'dak-kaw',
'H1794': 'daka',
'H1795': 'dakah (daw-kaw)',
'H1796': 'dokiy (dok-ee)',
'H1797': 'dek (dake)',
'H1798': 'dikken (dik-kane)',
'H1799': 'dikkeh (dik-keh)',
'H1800': 'dal (dal)',
# --- Batch H1801-H2000 (Simple Format w/ Meaning) ---
'H1801': 'dalag (leap)',
'H1802': 'dalah (to draw water)',
'H1803': 'daliy (a bucket)',
'H1804': 'daliyah (branch, bough)',
'H1805': 'Dalphown (Dalphon)',
'H1806': 'dalach (to stir up water)',
'H1807': 'Delayah (Delaiah)',
'H1808': 'Delayahu (Delaiah)',
'H1809': 'daliy (bough, branch)',
'H1810': 'daliyoth (branches)',
'H1811': 'dalal (to be low, hang)',
'H1812': 'dalaph (to drip, drop)',
'H1813': 'deleph (a dropping)',
'H1814': 'dalaq (to burn, pursue)',
'H1815': 'delaq (burning fever)',
'H1816': 'dallaqeth (inflammation)',
'H1817': 'deleth (door, gate)',
'H1818': 'dam (blood)',
'H1819': 'damah (to be like, resemble)',
'H1820': 'damah (to cease, be silent)',
'H1821': 'damam (to be silent, still)',
'H1822': 'demam (stillness)',
'H1823': 'demamah (stillness, calm)',
'H1824': 'demiy (silence, rest)',
'H1825': 'dimyown (likeness)',
'H1826': 'dama (to weep)',
'H1827': 'dimah (tears)',
'H1828': 'demea (tears, juice)',
'H1829': 'damesheq (activity, damask)',
'H1830': 'Damesheq (Damascus)',
'H1831': 'Dammeseq (Damascus)',
'H1832': 'dema (juice)',
'H1833': 'dimna (dunghill)',
'H1834': 'Dimnah (Dimnah)',
'H1835': 'Dan (Dan)',
'H1836': 'den (this)',
'H1837': 'den (this)',
'H1838': 'dannah (this)',
'H1839': 'Dani (Danite)',
'H1840': 'Daniyeel (Daniel)',
'H1841': 'Daniyeel (Daniel)',
'H1842': 'Dan-yaan (Dan-jaan)',
'H1843': 'dea (knowledge)',
'H1844': 'deah (knowledge)',
'H1845': 'daabown (fainting)',
'H1846': 'daag (to be anxious, fear)',
'H1847': 'deagah (anxiety, care)',
'H1848': 'daah (to fly rapidly)',
'H1849': 'daah (to fly)',
'H1850': 'dayah (a bird of prey)',
'H1851': 'dek (crushed)',
'H1852': 'dakar (to pierce, thrust through)',
'H1853': 'deqen (this)',
'H1854': 'daka (to crush)',
'H1855': 'dekak (to crush in pieces)',
'H1856': 'daqar (to stab)',
'H1857': 'deqer (a piercing)',
'H1858': 'daq (thin, small, fine)',
'H1859': 'daq (thin, small)',
'H1860': 'doq (a veil, curtain)',
'H1861': 'dar (pearl, mother-of-pearl)',
'H1862': 'dar (generation)',
'H1863': 'darbown (goad)',
'H1864': 'darda (thistle)',
'H1865': 'darowm (south, south wind)',
'H1866': 'derowr (swallow, bird)',
'H1867': 'Derowr (liberty, release)',
'H1868': 'derek (way, road, path)',
'H1869': 'derek (way, road)',
'H1870': 'darak (to tread, bend the bow)',
'H1871': 'darek (your way)',
'H1872': 'Darkown (Darkon)',
'H1873': 'darad (to flow)',
'H1874': 'dara (generation)',
'H1875': 'darash (to seek, inquire)',
'H1876': 'dasha (to sprout, spring up)',
'H1877': 'deshe (young grass)',
'H1878': 'dashen (to be fat, prosper)',
'H1879': 'dashen (fat, rich)',
'H1880': 'deshen (fatness, ashes)',
'H1881': 'dath (law, decree)',
'H1882': 'dath (law, decree)',
'H1883': 'Dathan (Dathan)',
'H1884': 'dethe (grass)',
'H1885': 'Dothan (Dothan)',
'H1886': 'Dothayin (Dothan)',
'H1887': 'he (the, this, that)',
'H1888': 'he (lo! behold!)',
'H1889': 'heach (ah! alas!)',
'H1890': 'habhab (cakes)',
'H1891': 'habal (to act vainly, become vain)',
'H1892': 'hebel (vanity, breath)',
'H1893': 'hebel (vapor, breath)',
'H1894': 'Hebel (Abel)',
'H1895': 'habal (to be, become vain)',
'H1896': 'haben (ebony)',
'H1897': 'hoben (ebony)',
'H1898': 'habar (to divide)',
'H1899': 'hagar (to gird)',
'H1900': 'Hagar (Hagar)',
'H1901': 'Hagriy (Hagrite)',
'H1902': 'Hagriy (Hagrite)',
'H1903': 'Hagri (Hagri)',
'H1904': 'had (a sound)',
'H1905': 'had (Had)',
'H1906': 'hadab (to stretch out)',
'H1907': 'hadabar (minister)',
'H1908': 'Hedad (Hadad)',
'H1909': 'Hedad (Hadad)',
'H1910': 'Hadoram (Hadoram)',
'H1911': 'hadah (to lead, guide)',
'H1912': 'hadom (footstool)',
'H1913': 'Haduwr (Hador)',
'H1914': 'Haday (Hadai)',
'H1915': 'hadaph (to thrust, drive away)',
'H1916': 'hadar (to honor, adorn)',
'H1917': 'hadar (ornament, splendor)',
'H1918': 'Hadar (Hadar)',
'H1919': 'Hadar (Hadar)',
'H1920': 'Hadar (Hadar)',
'H1921': 'hadar (glory, majesty)',
'H1922': 'Hadar (Hadar)',
'H1923': 'hadarah (adornment, glory)',
'H1924': 'Hadarezer (Hadarezer)',
'H1925': 'Hadoram (Hadoram)',
'H1926': 'hadar (to honor, adorn)',
'H1927': 'hadarah (honor, majesty)',
'H1928': 'Haddad (Hadad)',
'H1929': 'Hadad (Hadad)',
'H1930': 'Hoduw (India)',
'H1931': 'huw (he, she, it)',
'H1932': 'huw (he, she, it)',
'H1933': 'hava (to be, become)',
'H1934': 'hava (to be, become)',
'H1935': 'howd (splendor, majesty)',
'H1936': 'Howd (Hod)',
'H1937': 'Howdavyah (Hodaviah)',
'H1938': 'Howdavyahu (Hodaviah)',
'H1939': 'Howdevah (Hodevah)',
'H1940': 'Howdiyah (Hodiah)',
'H1941': 'huvah (ruin, mischief)',
'H1942': 'havvah (desire, ruin)',
'H1943': 'havvah (calamity, destruction)',
'H1944': 'Howah (disaster)',
'H1945': 'howy (ah! alas! woe!)',
'H1946': 'howlal (madness)',
'H1947': 'howlelah (madness)',
'H1948': 'howm (to make noise)',
'H1949': 'huwm (to make noise, resound)',
'H1950': 'hown (wealth, substance)',
'H1951': 'huwn (to be ready, easy)',
'H1952': 'hawa (to desire, breathe)',
'H1953': 'hawa (to fall)',
'H1954': 'howsha (save!)',
'H1955': 'Howshea (Hosea)',
'H1956': 'Howshama (Hoshama)',
'H1957': 'howthiyr (to leave, remain)',
'H1958': 'hi (she, it)',
'H1959': 'hi (lamentation)',
'H1960': 'hayah (woe! alas!)',
'H1961': 'hayah (to be, become)',
'H1962': 'hayah (calamity)',
'H1963': 'heykal (palace, temple)',
'H1964': 'heykal (palace, temple)',
'H1965': 'heykal (palace, temple)',
'H1966': 'hiylel (praise)',
'H1967': 'Heylel (Heylel, Lucifer)',
'H1968': 'hiyn (a hin, liquid measure)',
'H1969': 'hiyn (a hin)',
'H1970': 'hakkarah (look, appearance)',
'H1971': 'hakkar (to recognize)',
'H1972': 'hakkir (to recognize)',
'H1973': 'hal (hither, this way)',
'H1974': 'hala (further, beyond)',
'H1975': 'hale (hither)',
'H1976': 'hele (this)',
'H1977': 'halaz (that)',
'H1978': 'halazeh (this)',
'H1979': 'halazuw (these)',
'H1980': 'halak (to go, walk, come)',
'H1981': 'halak (to go, walk)',
'H1982': 'helek (a going, journey)',
'H1983': 'helek (traveler)',
'H1984': 'halakah (journey)',
'H1985': 'haliykah (a going, procession)',
'H1986': 'halam (to strike, beat)',
'H1987': 'halmuth (hammer, mallet)',
'H1988': 'halom (hither, here)',
'H1989': 'hem (they, these)',
'H1990': 'hem (they, these)',
'H1991': 'hem (their)',
'H1992': 'hem (they, these)',
'H1993': 'hamah (to murmur, growl, roar)',
'H1994': 'hamown (multitude, crowd)',
'H1995': 'hamown (noise, tumult, crowd)',
'H1996': 'Hamownah (Hamonah)',
'H1997': 'Hamown Gowg (Hamon-gog)',
'H1998': 'hemiyah (sound, roaring)',
'H1999': 'hamam (to make noise, confuse)',
'H2000': 'hen (they, these)',
# --- Batch H2001-H2200 (Simple Format w/ Meaning) ---
'H2001': 'hen (lo! behold!)',
'H2002': 'hen (if, whether)',
'H2003': 'hennah (they, these)',
'H2004': 'hinnats (hence, hither)',
'H2005': 'hennah (hither, here)',
'H2006': 'hinneh (lo! behold!)',
'H2007': 'hen (they, these)',
'H2008': 'Hen (Hen)',
'H2009': 'Hena (Hena)',
'H2010': 'henadad (Hadad is favor)',
'H2011': 'Hinnom (Hinnom)',
'H2012': 'hes (hush! keep silence!)',
'H2013': 'hasah (to be silent)',
'H2014': 'haphak (to turn, overthrow)',
'H2015': 'hephek (the contrary, opposite)',
'H2016': 'hephek (perversity)',
'H2017': 'haphakpak (crooked)',
'H2018': 'haphekah (overthrow)',
'H2019': 'Hapharaim (Hapharaim)',
'H2020': 'hatstsalah (deliverance)',
'H2021': 'hetsen (a weapon)',
'H2022': 'har (mountain, hill)',
'H2023': 'hor (mountain)',
'H2024': 'Har (Hor)',
'H2025': 'hara (mountain)',
'H2026': 'harag (to kill, slay)',
'H2027': 'hereg (a slaughter)',
'H2028': 'haregah (slaughter)',
'H2029': 'harah (to conceive, be pregnant)',
'H2030': 'hareh (pregnant)',
'H2031': 'harhor (thought)',
'H2032': 'herown (conception, pregnancy)',
'H2033': 'harowr (parched)',
'H2034': 'hariysah (overthrow, ruin)',
'H2035': 'hariysuth (overthrow)',
'H2036': 'Haram (Haram)',
'H2037': 'harel (mountain of God)',
'H2038': 'haram (to destroy utterly)',
'H2039': 'Horem (Horem)',
'H2040': 'haram (to destroy utterly)',
'H2041': 'Harim (Harim)',
'H2042': 'harar (mountain, hill country)',
'H2043': 'Harari (Hararite)',
'H2044': 'haras (to pull down, destroy)',
'H2045': 'heres (destruction)',
'H2046': 'Haran (Haran)',
'H2047': 'Haran (Haran)',
'H2048': 'harer (mountain)',
'H2049': 'haras (to pull down)',
'H2050': 'hathath (terror)',
'H2051': 'Vadon (Vadon)',
'H2052': 'vaday (certainly)',
'H2053': 'vav (and, but, also)',
'H2054': 'vazar (a courtier)',
'H2055': 'Vayzatha (Vajezatha)',
'H2056': 'valad (child)',
'H2057': 'valad (child)',
'H2058': 'Vopshiy (Vophsi)',
'H2059': 'Vashni (Vashni)',
'H2060': 'Vashtiy (Vashti)',
'H2061': 'zeb (wolf)',
'H2062': 'Zeeb (Zeeb)',
'H2063': 'zoth (this, that)',
'H2064': 'zabad (to endow, bestow)',
'H2065': 'zebed (a gift, dowry)',
'H2066': 'Zabad (Zabad)',
'H2067': 'Zabdiy (Zabdi)',
'H2068': 'Zabdiyel (Zabdiel)',
'H2069': 'zebuwl (dwelling, habitation)',
'H2070': 'zebuwluwn (dwelling)',
'H2071': 'zebach (to slaughter, sacrifice)',
'H2072': 'zebach (a sacrifice)',
'H2073': 'zebach (a sacrifice)',
'H2074': 'Zebuwluwn (Zebulun)',
'H2075': 'Zebuwluniy (Zebulunite)',
'H2076': 'zebub (a fly)',
'H2077': 'zebach (sacrifice)',
'H2078': 'Zebach (Zebah)',
'H2079': 'zaban (to buy)',
'H2080': 'zebuwl (dwelling)',
'H2081': 'zebul (dwelling)',
'H2082': 'Zebuwl (Zebul)',
'H2083': 'Zebul (Zebul)',
'H2084': 'zag (grape-skin)',
'H2085': 'zed (proud, arrogant)',
'H2086': 'zed (proud, arrogant)',
'H2087': 'zadown (pride, presumption)',
'H2088': 'zeh (this, that)',
'H2089': 'zeh (this, that)',
'H2090': 'zeh (that)',
'H2091': 'zahab (gold)',
'H2092': 'zahab (gold)',
'H2093': 'zaham (to be foul, loathsome)',
'H2094': 'zahar (to warn, admonish)',
'H2095': 'zahar (to warn)',
'H2096': 'zohar (brightness, splendor)',
'H2097': 'zu (this, that)',
'H2098': 'zu (this)',
'H2099': 'zuv (to flow, gush)',
'H2100': 'zowb (a flowing, issue)',
'H2101': 'zuwd (to boil, act proudly)',
'H2102': 'zuwd (to act proudly)',
'H2103': 'zuwlah (besides, except)',
'H2104': 'zuwlah (removal)',
'H2105': 'zuwn (to feed)',
'H2106': 'zuwa (to move, tremble)',
'H2107': 'zuwa (to tremble)',
'H2108': 'zuwr (to be a stranger)',
'H2109': 'zuwr (to be strange)',
'H2110': 'zuwr (strange, foreign)',
'H2111': 'zuwa (to remove)',
'H2112': 'zuwr (to press, crush)',
'H2113': 'zuwr (cud)',
'H2114': 'zuwr (strange, foreign)',
'H2115': 'zuwr (strangeness)',
'H2116': 'zuwth (loathsome)',
'H2117': 'zayith (olive, olive tree)',
'H2118': 'zach (pure, clean)',
'H2119': 'zachah (to be pure, clean)',
'H2120': 'zachuw (pure)',
'H2121': 'zachak (to be white)',
'H2122': 'zacha (to be pure)',
'H2123': 'zakak (to be bright, pure)',
'H2124': 'Zakuwr (Zaccur)',
'H2125': 'Zakuwr (Zaccur)',
'H2126': 'zakuwr (male)',
'H2127': 'zakiy (pure, clean)',
'H2128': 'Zakkay (Zaccai)',
'H2129': 'zawkak (to be bright)',
'H2130': 'zakukith (glass)',
'H2131': 'zakah (to be clean, pure)',
'H2132': 'zakah (to be pure)',
'H2133': 'zakiy (pure)',
'H2134': 'zakuw (purity)',
'H2135': 'zakiy (pure)',
'H2136': 'Zeker (Zeker)',
'H2137': 'Zeker (Zeker)',
'H2138': 'zalag (to be agitated)',
'H2139': 'zalaphah (burning heat)',
'H2140': 'Zeleph (Zeleph)',
'H2141': 'zakar (to remember)',
'H2142': 'zakar (to remember)',
'H2143': 'zeker (remembrance, memorial)',
'H2144': 'zakar (male)',
'H2145': 'zikrown (memorial, record)',
'H2146': 'zikarown (memorial, remembrance)',
'H2147': 'Zekaryah (Zechariah)',
'H2148': 'Zekaryahu (Zechariah)',
'H2149': 'zulluth (vileness)',
'H2150': 'zalzal (twig, branch)',
'H2151': 'zalal (to be worthless, vile)',
'H2152': 'zalaphah (glowing heat)',
'H2153': 'zilpah (a trickling)',
'H2154': 'Zilpah (Zilpah)',
'H2155': 'Zilpa (Zilpah)',
'H2156': 'zammah (plan, wickedness)',
'H2157': 'zamam (to purpose, devise)',
'H2158': 'zamam (plan, device)',
'H2159': 'zamzam (plotter)',
'H2160': 'Zamzummiym (Zamzummim)',
'H2161': 'zaman (to appoint, fix a time)',
'H2162': 'zeman (time, season)',
'H2163': 'zaman (to agree)',
'H2164': 'zeman (time)',
'H2165': 'zaman (to prepare)',
'H2166': 'zemar (to pluck, prune)',
'H2167': 'zamar (to sing, praise)',
'H2168': 'zamar (to make music)',
'H2169': 'zemar (music)',
'H2170': 'zemer (music)',
'H2171': 'zemorah (branch, twig)',
'H2172': 'zamar (song)',
'H2173': 'zammar (singer)',
'H2174': 'zammar (singer)',
'H2175': 'zimrah (music, song)',
'H2176': 'zimrah (choice products)',
'H2177': 'Zimran (Zimran)',
'H2178': 'Zimriy (Zimri)',
'H2179': 'Zimriy (Zimri)',
'H2180': 'Zimriy (Zimri)',
'H2181': 'zanav (to cut off the tail)',
'H2182': 'zanav (tail)',
'H2183': 'zanab (tail)',
'H2184': 'zanach (to reject, spurn)',
'H2185': 'zenuwth (fornication)',
'H2186': 'zanuwn (fornication)',
'H2187': 'zanach (to reject)',
'H2188': 'zanach (to remove)',
'H2189': 'zanah (to commit fornication)',
'H2190': 'zaan (to be angry)',
'H2191': 'zaaph (to be angry, rage)',
'H2192': 'zaaph (hot, raging)',
'H2193': 'zaaph (storm, rage)',
'H2194': 'zaaq (to cry, call out)',
'H2195': 'zaaq (to cry out)',
'H2196': 'zaaq (cry, outcry)',
'H2197': 'zaaqah (a cry, outcry)',
'H2198': 'zaqun (old age)',
'H2199': 'zaqan (to be old)',
'H2200': 'zoqen (old age)',
# --- Batch H2201-H2400 (Simple Format w/ Meaning) ---
'H2201': 'zaqeph (to lift up, raise)',
'H2202': 'zeqeph (to lift up)',
'H2203': 'zaqaph (impale, hang)',
'H2204': 'zaqen (old, aged)',
'H2205': 'zaqen (old man, elder)',
'H2206': 'ziqnah (old age)',
'H2207': 'zaqun (old age)',
'H2208': 'zaqaq (to refine, purify)',
'H2209': 'zeqeq (fetters)',
'H2210': 'zar (stranger, foreigner)',
'H2211': 'zar (strange, foreign)',
'H2212': 'zar (stranger)',
'H2213': 'zer (wreath, border)',
'H2214': 'zara (to scatter, disperse)',
'H2215': 'zara (to be scattered)',
'H2216': 'zara (to scatter)',
'H2217': 'zarab (to be heated)',
'H2218': 'zereb (heat)',
'H2219': 'zarah (to scatter, winnow)',
'H2220': 'zarow (sowing time)',
'H2221': 'zarziyr (girt, agile)',
'H2222': 'zarach (to rise, shine)',
'H2223': 'zerach (a rising, dawning)',
'H2224': 'Zerach (Zerah)',
'H2225': 'Zerach (Zerah)',
'H2226': 'Zarchy (Zarhite)',
'H2227': 'Zarechyah (Zerahiah)',
'H2228': 'zaram (to pour forth, gush)',
'H2229': 'zerem (a flood, downpour)',
'H2230': 'ziremah (a flowing, issue)',
'H2231': 'zera (seed, offspring)',
'H2232': 'zara (to sow)',
'H2233': 'zera (seed, sowing)',
'H2234': 'zerua (a sowing)',
'H2235': 'zeroa (arm, shoulder, strength)',
'H2236': 'zara (to be sown)',
'H2237': 'zaraph (to flow)',
'H2238': 'zereth (a span)',
'H2239': 'Zeresh (Zeresh)',
'H2240': 'Zeruah (Zeruah)',
'H2241': 'zera (sowing)',
'H2242': 'Zebadyah (Zebadiah)',
'H2243': 'Zebadyahu (Zebadiah)',
'H2244': 'Zabdi (Zabdi)',
'H2245': 'Zebedee (Zebedee)',
'H2246': 'Zebina (Zebina)',
'H2247': 'chab (bosom)',
'H2248': 'chaba (to hide)',
'H2249': 'chabab (to love)',
'H2250': 'chabab (to hide)',
'H2251': 'chob (bosom)',
'H2252': 'chabah (to hide oneself)',
'H2253': 'chobah (a hiding place)',
'H2254': 'chabal (to bind, pledge)',
'H2255': 'chabal (to act corruptly)',
'H2256': 'chebel (rope, cord, portion)',
'H2257': 'chabol (pledge, debt)',
'H2258': 'chabolah (pledge)',
'H2259': 'chibbel (mast)',
'H2260': 'chabat (to beat out, thresh)',
'H2261': 'chabatstseleth (lily, crocus)',
'H2262': 'Chabatstsanyah (Haba-zziniah)',
'H2263': 'chabaq (to embrace, fold hands)',
'H2264': 'chibbuq (a clasping, embrace)',
'H2265': 'Chabaqquwq (Habakkuk)',
'H2266': 'chabar (to unite, join)',
'H2267': 'cheber (association, company)',
'H2268': 'Cheber (Heber)',
'H2269': 'Cheber (Heber)',
'H2270': 'chaber (associate, companion)',
'H2271': 'chabbar (partner, associate)',
'H2272': 'chabbuwrah (stripe, wound)',
'H2273': 'chabereth (companion)',
'H2274': 'Chebrown (Hebron)',
'H2275': 'Chebrown (Hebron)',
'H2276': 'Chebrowniy (Hebronite)',
'H2277': 'chaber (companion)',
'H2278': 'chaber (companion)',
'H2279': 'chaber (companion)',
'H2280': 'chabash (to bind, gird, saddle)',
'H2281': 'chabeth (flat plate, pan)',
'H2282': 'chag (festival, feast)',
'H2283': 'chagab (locust)',
'H2284': 'chagab (locust)',
'H2285': 'chagav (cleft, hiding place)',
'H2286': 'chagag (to hold a feast)',
'H2287': 'chagag (to hold a feast)',
'H2288': 'chagowr (a girdle)',
'H2289': 'chagowr (girdle, belt)',
'H2290': 'chagowrah (girdle, apron)',
'H2291': 'Chagiy (Haggi)',
'H2292': 'Chaggay (Haggai)',
'H2293': 'Chaggith (Haggith)',
'H2294': 'Chaggiy (Haggite)',
'H2295': 'Chaggiyah (Haggiah)',
'H2296': 'chad (one)',
'H2297': 'chad (one)',
'H2298': 'chad (one)',
'H2299': 'chad (one)',
'H2300': 'chadad (to be sharp, keen)',
'H2301': 'chadad (to sharpen)',
'H2302': 'chad (sharp)',
'H2303': 'chadduwd (pointed, sharp)',
'H2304': 'chadad (to be sharp)',
'H2305': 'chadah (to rejoice)',
'H2306': 'Chadiyd (Hadid)',
'H2307': 'chad (one)',
'H2308': 'chadal (to cease, forbear)',
'H2309': 'chedel (the world, duration)',
'H2310': 'chadel (ceasing, frail)',
'H2311': 'Chadel (Hadel)',
'H2312': 'Chadlay (Hadlai)',
'H2313': 'chadaq (thorn, brier)',
'H2314': 'Chedeq (Hedek)',
'H2315': 'chadar (to enclose, surround)',
'H2316': 'cheder (chamber, room)',
'H2317': 'Chadar (Hadar)',
'H2318': 'chadash (to be new, renew)',
'H2319': 'chadash (new, fresh)',
'H2320': 'chodesh (new moon, month)',
'H2321': 'chodesh (new)',
'H2321': 'Chodesh (Hodesh)',
'H2323': 'chadath (new)',
'H2324': 'chadath (new)',
'H2325': 'chuwb (to be guilty, owe)',
'H2326': 'chowb (debt)',
'H2327': 'Chowb (Hob)',
'H2328': 'chuwbah (debt)',
'H2329': 'Chowbab (Hobab)',
'H2330': 'chuwg (to encircle)',
'H2331': 'chuwg (circle, vault)',
'H2332': 'chuwg (circle)',
'H2333': 'Chuwgah (Hugah)',
'H2334': 'chuwd (to propose a riddle)',
'H2335': 'chuwd (to tell)',
'H2336': 'chowd (splendor)',
'H2337': 'chavah (to tell, declare)',
'H2338': 'chavah (to show)',
'H2339': 'chizzayown (vision)',
'H2340': 'chuwach (thorn-bush)',
'H2341': 'Chuwach (Huah)',
'H2342': 'chuwl (to twist, whirl, dance)',
'H2343': 'chuwl (sand)',
'H2344': 'chowl (sand)',
'H2345': 'Chuwm (Hum)',
'H2346': 'chowm (brown)',
'H2347': 'chuwmah (wall)',
'H2348': 'chuwn (to be gracious)',
'H2349': 'chuwn (treasure)',
'H2350': 'chuwc (to pity, spare)',
'H2351': 'chuwts (outside, street)',
'H2352': 'chuwts (outside)',
'H2353': 'chuwq (to cut in)',
'H2354': 'chuwr (to be or grow white)',
'H2355': 'chuwr (white stuff, linen)',
'H2356': 'chuwr (a hole)',
'H2357': 'chuwr (noble)',
'H2358': 'Chuwr (Hur)',
'H2359': 'Chuwr (Hur)',
'H2360': 'Chuwray (Hurai)',
'H2361': 'Chuwr-chown (Hur-hon)',
'H2362': 'chuwsh (to hasten, hurry)',
'H2363': 'chuwsh (to hasten)',
'H2364': 'Chuwshah (Hushah)',
'H2365': 'Chuwshay (Hushai)',
'H2366': 'Chuwshiym (Hushim)',
'H2367': 'Chuwshiym (Hushim)',
'H2368': 'chuwth (to snatch)',
'H2369': 'chaza (to see, behold)',
'H2370': 'chaza (to see)',
'H2371': 'chazayahu (Hazaiah)',
'H2372': 'chazah (to see, behold)',
'H2373': 'chozeh (seer)',
'H2374': 'chozeh (seer)',
'H2375': 'chazow (vision)',
'H2376': 'chazeh (breast of animal)',
'H2377': 'chazown (vision)',
'H2378': 'chazuw (vision)',
'H2379': 'chazuw (vision)',
'H2380': 'chazowth (vision)',
'H2381': 'chazowth (conspicuous)',
'H2382': 'chazaq (to be strong, seize)',
'H2383': 'chezeq (strength)',
'H2384': 'chezqah (strength, force)',
'H2385': 'chezqah (strength)',
'H2386': 'chazaq (strong, mighty)',
'H2387': 'chazaq (strong)',
'H2388': 'chazaq (to be strong, hard)',
'H2389': 'chazaq (strong, mighty)',
'H2390': 'chozeq (strength)',
'H2391': 'chezeq (strength)',
'H2392': 'chozqah (strength, force)',
'H2393': 'chizeq (to strengthen)',
'H2394': 'Chizqiy (Hizki)',
'H2395': 'Chizqiyah (Hiskiah)',
'H2396': 'Chizqiyahu (Hezekiah)',
'H2397': 'chay (alive, living)',
'H2398': 'chata (to sin, miss)',
'H2399': 'chet (sin, sin offering)',
'H2400': 'chata (sin)',
'H2401': 'a sin (chataah)',
'H2402': 'a sin (chattaah)',
'H2403': 'sin, sin offering (chattath)',
'H2404': 'sinner (chattaya)',
'H2405': 'sinful (chatta)',
'H2406': 'to snatch, seize (chataph)',
'H2407': 'robbery (chetaph)',
'H2408': 'to dig, search (chatar)',
'H2409': 'an expiation (chattaya)',
'H2410': 'explorer (Chatiyta)',
'H2411': 'fluctuating (Chattiyl)',
'H2412': 'robber (Chatiypha)',
'H2413': 'to stop (chatam)',
'H2414': 'to clutch (chataph)',
'H2415': 'a twig (choter)',
'H2416': 'alive (chay)',
'H2417': 'alive (chay)',
'H2418': 'to live (chaya)',
'H2419': 'living of God (Chiyel)',
'H2420': 'a puzzle (chiydah)',
'H2421': 'to live (chayah)',
'H2422': 'vigorous (chayeh)',
'H2423': 'an animal (cheyva)',
'H2424': 'life (chayuwth)',
'H2425': 'to live (chayay)',
'H2426': 'an army (cheyl)',
'H2427': 'a throe (chiyl)',
'H2428': 'a force, wealth, army (chayil)',
'H2429': 'an army, or strength (chayil)',
'H2430': 'an intrenchment (cheylah)',
'H2431': 'fortress (Cheylam)',
'H2432': 'fortress (Chiylen)',
'H2433': 'beauty (chiyn)',
'H2434': 'a wall (chayits)',
'H2435': 'outer, exterior (chiytsown)',
'H2436': 'bosom, lap (cheyq)',
'H2437': 'Chirah (Chiyrah)',
'H2438': 'Chiram, Huram (Chiyram)',
'H2439': 'to hurry (chiysh)',
'H2440': 'a hurry, quickly (chiysh)',
'H2441': 'palate, mouth (chek)',
'H2442': 'to wait, long for (chakah)',
'H2443': 'a hook, angle (chakkah)',
'H2444': 'dark (Chakiylah)',
'H2445': 'wise, a Magian (chakkiym)',
'H2446': 'darkness of Jah (Chakalyah)',
'H2447': 'darkly flashing, red (chakliyl)',
'H2448': 'flash, redness (chakliluwth)',
'H2449': 'to be wise (chakam)',
'H2450': 'wise, skilful (chakam)',
'H2451': 'wisdom (chokmah)',
'H2452': 'wisdom (chokmah)',
'H2453': 'skilful (Cahkmowniy)',
'H2454': 'wisdom (chokmowth)',
'H2455': 'exposed, profane, common (chol)',
'H2456': 'to be sick (chala)',
'H2457': 'disease, rust, scum (chelah)',
'H2458': 'Chelah (Chelah)',
'H2459': 'fat, richest part (cheleb)',
'H2460': 'fatness (Cheleb)',
'H2461': 'milk (chalab)',
'H2462': 'fertility (Chelbah)',
'H2463': 'fruitful (Chelbown)',
'H2464': 'galbanam (chelbnah)',
'H2465': 'life, age, world (cheled)',
'H2466': 'Cheled (cheled)',
'H2467': 'a weasel (choled)',
'H2468': 'Chuldah (Chuldah)',
'H2469': 'worldliness (Chelday)',
'H2470': 'to be weak, sick, afflicted (chalah)',
'H2471': 'a cake (challah)',
'H2472': 'a dream (chalowm)',
'H2473': 'sandy (Cholown)',
'H2474': 'window (challown)',
'H2475': 'surviving, orphans (chalowph)',
'H2476': 'defeat (chaluwshah)',
'H2477': 'Chalach (Chalach)',
'H2478': 'contorted (Chalchuwl)',
'H2479': 'writhing, pain (chalchalah)',
'H2480': 'to snatch at, catch (chalat)',
'H2481': 'a trinket, jewel (chaliy)',
'H2482': 'Chali (Chaliy)',
'H2483': 'malady, sickness, grief (choliy)',
'H2484': 'a trinket, jewel (chelyah)',
'H2485': 'flute, pipe (chaliyl)',
'H2486': 'far be it!, (God) forbid (chaliylah)',
'H2487': 'alternation, change (chaliyphah)',
'H2488': 'spoil, armor (chaliytsah)',
'H2489': 'wretch, poor (chelka)',
'H2490': 'to profane, defile, begin (chalal)',
'H2491': 'pierced, slain, polluted (chalal)',
'H2492': 'to dream (chalam)',
'H2493': 'a dream (chelem)',
'H2494': 'a dream (Chelem)',
'H2495': 'purslain, egg (challamuwth)',
'H2496': 'flint (challamiysh)',
'H2497': 'strong (Chelon)',
'H2498': 'to pass by, change, renew (chalaph)',
'H2499': 'to pass on (chalaph)',
'H2500': 'exchange, instead of (cheleph)',
'H2501': 'change (Cheleph)',
'H2502': 'to pull off, deliver, arm (chalats)',
'H2503': 'strength (Chelets)',
'H2504': 'loins (chalats)',
'H2505': 'to be smooth, divide, flatter (chalaq)',
'H2506': 'smoothness, allotment, portion (cheleq)',
'H2507': 'portion (Cheleq)',
'H2508': 'a part, portion (chalaq)',
'H2509': 'smooth, flattering (chalaq)',
'H2510': 'bare (Chalaq)',
'H2511': 'smooth (challaq)',
'H2512': 'smooth (challuq)',
'H2513': 'smoothness, field, portion (chelqah)',
'H2514': 'flattery (chalaqqah)',
'H2515': 'a distribution, division (chaluqqah)',
'H2516': 'a Chelkite (Chelqiy)',
'H2517': 'apportioned (Chelqay)',
'H2518': 'portion of Jah (Chilqiyah)',
'H2519': 'very smooth, slippery, flattery (chalaqlaqqah)',
'H2520': 'smoothness (Chelqath)',
'H2521': 'smoothness of the rocks (Chelqath hats-Tsu-riym)',
'H2522': 'to prostrate, overthrow, weaken (chalash)',
'H2523': 'frail, weak (challash)',
'H2524': 'a father-in-law (cham)',
'H2525': 'hot, warm (cham)',
'H2526': 'hot (Cham)',
'H2527': 'heat (chom)',
'H2528': 'anger, fury (chema)',
'H2529': 'curdled milk, butter (chemah)',
'H2530': 'to delight in, covet (chamad)',
'H2531': 'delight, pleasant (chemed)',
'H2532': 'delight, desirable, pleasant (chemdah)',
'H2533': 'pleasant (Chemdan)',
'H2534': 'heat, anger, poison (chemah)',
'H2535': 'heat, sun (chammah)',
'H2536': 'anger of God (Chammuwel)',
'H2537': 'father-in-law of dew (Chamuwtal)',
'H2538': 'pitied (Chamuwl)',
'H2539': 'Hamulites (Chamuwliy)',
'H2540': 'warm spring (Chammown)',
'H2541': 'violent, a robber (chamowts)',
'H2542': 'a wrapping, drawers (chammuwq)',
'H2543': 'a male donkey (chamowr)',
'H2544': 'donkey (Chamowr)',
'H2545': 'a mother-in-law (chamowth)',
'H2546': 'a lizard, snail (chomet)',
'H2547': 'low (Chumtah)',
'H2548': 'seasoned, salt provender (chamiyts)',
'H2549': 'fifth (chamiyshiy)',
'H2550': 'to commiserate, spare, pity (chamal)',
'H2551': 'commiseration, pity (chemlah)',
'H2552': 'to be hot, be warm (chamam)',
'H2553': 'a sun-pillar, image (chamman)',
'H2554': 'to be violent, maltreat (chamac)',
'H2555': 'violence, wrong, unjust gain (chamac)',
'H2556': 'to be pungent, sour, leavened (chamets)',
'H2557': 'ferment, leaven (chametz)',
'H2558': 'vinegar (chomets)',
'H2559': 'to wrap, turn, depart (chamaq)',
'H2560': 'to boil up, ferment (chamar)',
'H2561': 'wine (chemer)',
'H2562': 'wine (chamar)',
'H2563': 'a heap, clay, homer (chomer)',
'H2564': 'bitumen, slime (chemar)',
'H2565': 'a heap (chamorah)',
'H2566': 'red (Chamran)',
'H2567': 'to tax a fifth (chamash)',
'H2568': 'five (chamesh)',
'H2569': 'a fifth tax (chomesh)',
'H2570': 'the abdomen, fifth (rib) (chomesh)',
'H2571': 'staunch, armed (chamush)',
'H2572': 'fifty (chamishshiym)',
'H2573': 'a skin bottle (chemeth)',
'H2574': 'walled (Chamath)',
'H2575': 'hot springs (Chammath)',
'H2576': 'hot springs of Dor (Chammoth Dor)',
'H2577': 'a Chamathite (Chamathiy)',
'H2578': 'Chamath of Tsobah (Chamath Tsowbah)',
'H2579': 'Chamath of Rabbah (Chamath Rabbah)',
'H2580': 'favor, grace (chen)',
'H2581': 'grace (Chen)',
'H2582': 'favor of Hadad (Chenadad)',
'H2583': 'to incline, pitch, encamp (chanah)',
'H2584': 'favored (Channah)',
'H2585': 'initiated (Chanowk)',
'H2586': 'favored (Chanuwn)',
'H2587': 'gracious (channuwn)',
'H2588': 'a vault, prison (chanuwth)',
'H2589': 'supplication (channowth)',
'H2590': 'to spice, embalm (chanat)',
'H2591': 'wheat (chinta)',
'H2592': 'favor of God (Channiyel)',
'H2593': 'initiated, trained (chaniyk)',
'H2594': 'graciousness, favor (chaniynah)',
'H2595': 'a lance, spear (chaniyth)',
'H2596': 'to narrow, dedicate, train up (chanak)',
'H2597': 'consecration, dedication (chanukka)',
'H2598': 'initiation, consecration (chanukkah)',
'H2599': 'a Chanokite (Chanokiy)',
'H2600': 'gratis, without cause (chinnam)',
'H2601': 'Chanamel (Chanamel)',
'H2602': 'frost (chanamal)',
'H2603': 'to be gracious, favor (chanan)',
'H2604': 'to favor, make supplication (chanan)',
'H2605': 'favor (Chanan)',
'H2606': 'God has favored (Chananel)',
'H2607': 'gracious (Chananiy)',
'H2608': 'Jah has favored (Chananyah)',
'H2609': 'Chanes (Chanec)',
'H2610': 'to soil, defile, pollute (chaneph)',
'H2611': 'soiled, impious, hypocrite (chaneph)',
'H2612': 'moral filth, hypocrisy (choneph)',
'H2613': 'impiety, profaneness (chanuphah)',
'H2614': 'to be narrow, hang self (chanaq)',
'H2615': 'favored (Channathon)',
'H2616': 'to be kind, shew self merciful (chacad)',
'H2617': 'kindness, mercy (checed)',
'H2618': 'Chesed (Checed)',
'H2619': 'Jah has favored (Chacadyah)',
'H2620': 'to flee for protection, trust (chacah)',
'H2621': 'hopeful (Chocah)',
'H2622': 'confidence, trust (chacuwth)',
'H2623': 'kind, godly, holy (chaciyd)',
'H2624': 'a stork (chaciydah)',
'H2625': 'caterpillar, locust (chaciyl)',
'H2626': 'firm, strong (chaciyn)',
'H2627': 'deficient, wanting (chacciyr)',
'H2628': 'to consume (chacal)',
'H2629': 'to muzzle, stop (chacam)',
'H2630': 'to be compact, lay up (chacan)',
'H2631': 'to possess (chacan)',
'H2632': 'strength, power (checen)',
'H2633': 'wealth, riches, strength (chocen)',
'H2634': 'powerful, strong (chacon)',
'H2635': 'a clod, clay (chacaph)',
'H2636': 'a shred, round thing (chacpac)',
'H2637': 'to lack, fail, decrease (chacer)',
'H2638': 'lacking, destitute (chacer)',
'H2639': 'lack, poverty (checer)',
'H2640': 'poverty, want (chocer)',
'H2641': 'want (Chacrah)',
'H2642': 'deficiency, wanting (checrown)',
'H2643': 'pure, innocent (chaph)',
'H2644': 'to cover, do secretly (chapha)',
'H2645': 'to cover, overlay (chaphah)',
'H2646': 'a canopy, chamber (chuppah)',
'H2647': 'Chuppah (Chuppah)',
'H2648': 'to hasten away, tremble (chaphaz)',
'H2649': 'hasty flight (chippazown)',
'H2650': 'Chuppim (Chuppiym)',
'H2651': 'fists, hands, handful (chophen)',
'H2652': 'Chophni (Chophniy)',
'H2653': 'to cover (chophaph)',
'H2654': 'to delight in, desire (chaphets)',
'H2655': 'pleased with, willing (chaphets)',
'H2656': 'pleasure, desire, matter (chephets)',
'H2657': 'my delight (is) in her (Chephtsiy bahh)',
'H2658': 'to dig, search out, seek (chaphar)',
'H2659': 'to blush, be ashamed (chapher)',
'H2660': 'a pit of shame (Chepher)',
'H2661': 'mole, rat (chaphor)',
'H2662': 'a Chephrite (Chephriy)',
'H2663': 'double pit (Chapharayim)',
'H2664': 'to seek, search, disguise (chaphas)',
'H2665': 'search (chephes)',
'H2666': 'to spread loose, be free (chaphash)',
'H2667': 'a carpet, precious (Chophesh)',
'H2668': 'liberty, freedom (chuphshah)',
'H2669': 'prostration by sickness, several (chophshuwth)',
'H2670': 'exempt, free (chophshiy)',
'H2671': 'an arrow, wound (chets)',
'H2672': 'to cut, hew, dig (chatsab)',
'H2673': 'to divide, halve (chatsah)',
'H2674': 'village (Chatsowr)',
'H2675': 'new Chatsor (Chatsowr Chadattah)',
'H2676': 'middle, midnight (chatsowth)',
'H2677': 'half, middle (chetsiy)',
'H2678': 'an arrow (chitstsiy)',
'H2679': 'midst of the resting- places (Chatsiy ham-Mnuchowth)',
'H2680': 'a Chatsi-ham-Menachtite (Chatsiy ham-Mnachti)',
'H2681': 'a court or abode (chatsiyr)',
'H2682': 'grass, leek, herb (chatsiyr)',
'H2683': 'the bosom (chetsen)',
'H2684': 'arm, lap (chotsen)',
'H2685': 'to be severe, urgent (chatsaph)',
'H2686': 'to divide, shoot (an arrow) (chatsats)',
'H2687': 'gravel, an arrow (chatsats)',
'H2688': 'division of (the) palm-tree (Chatstsown Tamar)',
'H2689': 'a trumpet (chatsotsrah)',
'H2690': 'to blow, sound (a trumpet) (chatsar)',
'H2691': 'a yard, court, village (chatser)',
'H2692': 'village of Addar (Chatsar Addar)',
'H2693': 'village of Fortune (Chatsar Gaddah)',
'H2694': 'village of the middle (Chatsar hat-Tiykown)',
'H2695': 'enclosure (Chetsrow)',
'H2696': 'court-yard (Chetsrown)',
'H2697': 'a Chetsronite (Chetsrowniy)',
'H2698': 'yards (Chatserowth)',
'H2699': 'yards (Chatseriym)',
'H2700': 'village of death (Chatsarmaveth)',
'H2701': 'village of cavalry (Chatsar Cuwcah)',
'H2702': 'village of horses (Chatsar Cuwciym)',
'H2703': 'village of springs (Chatsar Eynown)',
'H2704': 'village of springs (Chatsar Eynan)',
'H2705': 'village of (the) fox (Chatsar Shuwal)',
'H2706': 'an enactment (choq)',
'H2707': 'to carve (chaqah)',
'H2708': 'appointed, custom, manner, ordinance, site, statute (chuqqah)',
'H2709': 'crooked (Chaquwpha)',
'H2710': 'to hack (chaqaq)',
'H2711': 'an enactment, a resolution (cheqeq)',
'H2712': 'appointed (Chuqqog)',
'H2713': 'to penetrate (chaqar)',
'H2714': 'examination, enumeration, deliberation (cheqer)',
'H2715': 'white or pure (chor)',
'H2716': 'excrement (chere)',
'H2717': 'to parch (through drought) (charab)',
'H2718': 'to demolish (charab)',
'H2719': 'drought (chereb)',
'H2720': 'parched or ruined (chareb)',
'H2721': 'drought or desolation (choreb)',
'H2722': 'desolate (Choreb)',
'H2723': 'drought (chorbah)',
'H2724': 'a desert (charabah)',
'H2725': 'parching heat (charabown)',
'H2726': 'Charbona or Charbonah (Charbowna)',
'H2727': 'to leap suddenly (charag)',
'H2728': 'the leaping insect (chargol)',
'H2729': 'to shudder with terror (charad)',
'H2730': 'fearful (chared)',
'H2731': 'fear, anxiety (charadah)',
'H2732': 'Charadah (Charadah)',
'H2733': 'a Charodite (Charodiy)',
'H2734': 'to glow or grow warm (charah)',
'H2735': 'hole of the cleft (Chor hagGidgad)',
'H2736': 'fearing Jah (Charhayah)',
'H2737': 'pierced (charuwz)',
'H2738': 'pointed (charuwl)',
'H2739': 'snub-nosed (charuwmaph)',
'H2740': 'a burning of anger (charown)',
'H2741': 'a Charuphite or inhabitant of Charuph (or Chariph) (Charuwphiy)',
'H2742': 'incised or (active) incisive (charuwts)',
'H2743': 'earnest (Charuwts)',
'H2744': 'inflammation (Charchuwr)',
'H2745': 'perhaps shining (Charchac)',
'H2746': 'fever (as hot) (charchur)',
'H2747': 'a chisel or graver (cheret)',
'H2748': 'a horoscopist (as drawing magical lines or circles) (chartom)',
'H2749': 'magician (chartom)',
'H2750': 'a burning (i.e. intense) anger (choriy)',
'H2751': 'white bread (choriy)',
'H2752': 'cave-dweller or troglodyte (Choriy)',
'H2753': 'Chori (Choriy)',
'H2754': 'cut out (or hollow) (chariyt)',
'H2755': 'excrements of doves {or perhaps rather the plural of a single word charapyown {khar-aw-yone} (charey-yowniym)',
'H2756': 'autumnal (Chariyph)',
'H2757': 'incisure or (passively) incised (chariyts)',
'H2758': 'ploughing or its season (chariysh)',
'H2759': 'quiet (chariyshiy)',
'H2760': 'to braid (charak)',
'H2761': 'to scorch (charak)',
'H2762': 'a net (cherek)',
'H2763': 'to seclude (charam)',
'H2764': 'physical (as shutting in) a net (cherem)',
'H2765': 'devoted (Chorem)',
'H2766': 'snub-nosed (Charim)',
'H2767': 'devoted (Chormah)',
'H2768': 'abrupt (Chermown)',
'H2769': 'Hermons (Chermowniym)',
'H2770': 'a sickle (as cutting) (chermesh)',
'H2771': 'parched (Charan)',
'H2772': 'a Choronite or inhabitant of Choronaim (Choroniy)',
'H2773': 'double cave-town (Choronayim)',
'H2774': 'Charnepher (Charnepher)',
'H2775': 'the itch (cheres)',
'H2776': 'shining (Cherec)',
'H2777': 'a potsherd (charcuwth)',
'H2778': 'to pull off (charaph.)',
'H2779': 'the crop gathered (choreph)',
'H2780': 'reproachful (Chareph)',
'H2781': 'contumely, disgrace, the pudenda (cherpah)',
'H2782': 'to point sharply (charats)',
'H2783': 'the loin (as the seat of strength) (charats)',
'H2784': 'a fetter (chartsubbah)',
'H2785': 'a sour grape (as sharp in taste) (chartsan)',
'H2786': 'to grate the teeth (charaq)',
'H2787': 'to glow (charar)',
'H2788': 'arid (charer)',
'H2789': 'a piece of pottery (cheres)',
'H2790': 'to scratch (charash)',
'H2791': 'magical craft (cheresh)',
'H2792': 'Cheresh (Cheresh)',
'H2793': 'a forest (perhaps as furnishing the material for fabric) (choresh)',
'H2794': 'a fabricator or mechanic (choresh)',
'H2795': 'deaf (whether literally or spir.) (cheresh)',
'H2796': 'a fabricator or any material (charash)',
'H2797': 'magician (Charsha)',
'H2798': 'mechanics, the name of a valley in Jerusalem (Charashiym)',
'H2799': 'mechanical work (charosheth)',
'H2800': 'Charosheth (Charosheth)',
'H2801': 'to engrave (charath)',
'H2802': 'forest (Chereth)',
'H2803': 'to plait or interpenetrate (chashab)',
'H2804': 'to regard (chashab)',
'H2805': 'a belt or strap (as being interlaced) (chesheb)',
'H2806': 'considerate judge (Chashbaddanah)',
'H2807': 'estimation (Chashubah)',
'H2808': 'contrivance (cheshbown)',
'H2809': 'Cheshbon (Cheshbown)',
'H2810': 'a contrivance (chishshabown)',
'H2811': 'Jah has regarded (Chashabyah)',
'H2812': 'inventiveness (Chashabnah)',
'H2813': 'thought of Jah (Chashabnyah)',
'H2814': 'to hush or keep quiet (chashah)',
'H2815': 'intelligent (Chashshuwb)',
'H2816': 'the dark (chashowk)',
'H2817': 'nakedness (Chasuwpha)',
'H2818': 'to be necessary (from the idea of convenience) (chashach)',
'H2819': 'necessity (chashchuwth)',
'H2820': 'to restrain (chasak)',
'H2821': 'to be dark (as withholding light) (chashak)',
'H2822': 'the dark (choshek)',
'H2823': 'dark (figuratively (chashok)',
'H2824': 'darkness (cheshkah)',
'H2825': 'darkness (chashekah)',
'H2826': 'to make (intrans. be) unsteady (chashal)',
'H2827': 'to weaken (chashal)',
'H2828': 'enriched (Chashum)',
'H2829': 'opulent (Cheshmown)',
'H2830': 'probably bronze or polished spectrum metal (chashmal)',
'H2831': 'apparently wealthy (chashman)',
'H2832': 'fertile (Chashmonah)',
'H2833': 'perhaps a pocket (as holding the Urim and Thummim) (choshen)',
'H2834': 'to strip off (chasaph)',
'H2835': 'drawn off (chasiph)',
'H2836': 'to cling (chashaq)',
'H2837': 'delight (chesheq)',
'H2838': 'attached (chashuq)',
'H2839': 'conjoined (chishshuq)',
'H2840': 'combined (chishshur)',
'H2841': 'a combination or gathering (chashrah)',
'H2842': 'dry grass (chashash)',
'H2843': 'a Chushathite or descendant of Chushah (Chushathiy)',
'H2844': 'crushed (chath)',
'H2845': 'terror (Cheth)',
'H2846': 'to lay hold of (chathah)',
'H2847': 'fear (chittah)',
'H2848': 'swathed (chittuwl)',
'H2849': 'terror (chathchath)',
'H2850': 'a Chittite (Chittiy)',
'H2851': 'fear (chittiyth)',
'H2852': 'to cut off (chathak)',
'H2853': 'to swathe (chathal)',
'H2854': 'a swathing cloth (figuratively) (chathullah)',
'H2855': 'enswathed (Chethlon)',
'H2856': 'to close up (chatham)',
'H2857': 'to seal (chatham)',
'H2858': 'a seal (chothemeth)',
'H2859': 'to give (a daughter) away in marriage (chathan)',
'H2860': 'a relative by marriage (especially through the bride) (chathan)',
'H2861': 'a wedding (chathunnah)',
'H2862': 'to clutch (chathaph)',
'H2863': 'rapine (chetheph)',
'H2864': 'to force a passage (chathar)',
'H2865': 'to prostrate (chathath)',
'H2866': 'dismay (chathath)',
'H2867': 'Chathath (Chathath)',
'H2868': 'to rejoice (teb)',
'H2869': 'good (tab)',
'H2870': 'pleasing (to) God (tabel)',
'H2871': 'dyed (tabuwl)',
'H2872': 'accumulated (tabbuwr)',
'H2873': 'to slaughter (animals or men) (tabach)',
'H2874': 'something slaughtered (tebach)',
'H2875': 'massacre (Tebach)',
'H2876': 'a butcher (tabbach)',
'H2877': 'a lifeguardsman (tabbach)',
'H2878': 'flesh, slaughter (tibchah)',
'H2879': 'a female cook (tabbachah)',
'H2880': 'slaughter (Tibchath)',
'H2881': 'to dip, to immerse (tabal)',
'H2882': 'Jah has dipped (Tbalyahuw)',
'H2883': 'to sink (taba)',
'H2884': 'rings (Tabbaowth)',
'H2885': 'a seal (as sunk into the wax) (tabbaath)',
'H2886': 'pleasing (to) Rimmon (Tabrimmown)',
'H2887': 'Tebeth (Tebeth)',
'H2888': 'Tabbath (Tabbath)',
'H2889': 'pure (in a physical, chemical, ceremonial or moral sense) (tahowr)',
'H2890': 'purity (thowr)',
'H2891': 'to be bright (taher)',
'H2892': 'literally brightness (tohar)',
'H2893': 'ceremonial purification (tohorah)',
'H2894': 'to sweep away (tuw)',
'H2895': 'be (do) better, cheer, be (do, seem) good, (make) goodly, X please, (be, do, go, play) well (towb)',
'H2896': 'good (as an adjective) in the widest sense (towb)',
'H2897': 'good (Towb)',
'H2898': 'good, in the widest sense (tuwb)',
'H2899': 'pleasing (to) Adonijah (Towb Adoniyahuw)',
'H2900': 'goodness of Jehovah (Towbiyah)',
'H2901': 'to spin (tavah)',
'H2902': 'to smear (tuwach)',
'H2903': 'a fillet for the forehead (towphaphah)',
'H2904': 'to pitch over or reel (tuwl)',
'H2905': 'a row (tuwr)',
'H2906': 'a rock or hill (tuwr)',
'H2907': 'to pounce as a bird of prey (tuws)',
'H2908': 'hunger (as twisting) (tvath)',
'H2909': 'to stretch a bow (tachah)',
'H2910': 'the kidneys (as being covered) (tuwchah)',
'H2911': 'a hand mill (tchown)',
'H2912': 'to grind meal (tachan)',
'H2913': 'a hand mill (tachanah)',
'H2914': 'a boil or ulcer (from the inflammation) (tchor)',
'H2915': 'mortar or plaster (tiyach)',
'H2916': 'mud or clay (tiyt)',
'H2917': 'clay (tiyn)',
'H2918': 'a wall (tiyrah)',
'H2919': 'dew (as covering vegetation) (tal)',
'H2920': 'dew (tal)',
'H2921': 'to cover with pieces (tala)',
'H2922': 'a lamb (tla)',
'H2923': 'lambs (Tlaiym)',
'H2924': 'a lamb (taleh)',
'H2925': 'overthrow or rejection (taltelah)',
'H2926': 'to strew over (talal)',
'H2927': 'to cover with shade (tlal)',
'H2928': 'oppression (Telem)',
'H2929': 'oppressive (Talmown)',
'H2930': 'to be foul (tame)',
'H2931': 'foul in a relig. sense (tame)',
'H2932': 'religious impurity (tumah)',
'H2933': 'to be impure in a religious sense (tamah)',
'H2934': 'to hide (by covering over) (taman)',
'H2935': 'a basket (of interlaced osiers) (tene)',
'H2936': 'to soil (tanaph)',
'H2937': 'to wander (taah)',
'H2938': 'to taste (taam)',
'H2939': 'to taste (tam)',
'H2940': 'a taste (taam)',
'H2941': 'a taste (taam)',
'H2942': 'flavor (tem)',
'H2943': 'to load a beast (taan)',
'H2944': 'to stab (taan)',
'H2945': 'a family (mostly used collectively in the singular) (taph)',
'H2946': 'to flatten out or extend (as a tent) (taphach)',
'H2947': 'a spread of the hand (tephach)',
'H2948': 'hand-breadth (broad) (tophach)',
'H2949': 'nursing (tippuch)',
'H2950': 'to stick on as a patch (taphal)',
'H2951': 'a military governor (tiphcar)',
'H2952': 'apparently to trip (with short steps) coquettishly (taphaph)',
'H2953': 'a finger-nail (tphar)',
'H2954': 'apparently to be thick (taphash)',
'H2955': 'a dropping (of ointment) (Taphath)',
'H2956': 'to drive on (tarad)',
'H2957': 'to expel (trad)',
'H2958': 'not yet (trowm)',
'H2959': 'to overburden (tarach)',
'H2960': 'a burden (torach)',
'H2961': 'dripping (tariy)',
'H2962': 'non-occurrence (terem)',
'H2963': 'to pluck off or pull to pieces (taraph)',
'H2964': 'something torn (tereph)',
'H2965': 'recently torn off (taraph)',
'H2966': 'prey (trephah)',
'H2967': 'a Tarpelite (collectively) or inhabitants of Tarpel (Tarplay)',
'H2968': 'to desire (yaab)',
'H2969': 'to be suitable (yaah)',
'H2970': 'heard of Jah (Yaazanyah)',
'H2971': 'enlightener (Yaiyr)',
'H2972': 'a Jairite or descendant of Jair (Yairiy)',
'H2973': 'to be slack (yaal)',
'H2974': 'to yield, especially assent (yaal)',
'H2975': 'a channel (yor)',
'H2976': 'to desist (yaash)',
'H2977': 'founded of Jah (Yoshiyah)',
'H2978': 'an entry (yithown)',
'H2979': 'stepping (yathray)',
'H2980': 'to bawl (yabab)',
'H2981': 'produce (ybuwl)',
'H2982': 'trodden (Ybuwc)',
'H2983': 'a Jebusite or inhabitant of Jebus (Yebuwciy)',
'H2984': 'choice (Yibchar)',
'H2985': 'intelligent (Yabiyn)',
'H2986': 'to flow (yabal)',
'H2987': 'to bring (ybal)',
'H2988': 'a stream (yabal)',
'H2989': 'Jabal (Yabal)',
'H2990': 'having running sores (yabbel)',
'H2991': 'devouring people (Yiblam)',
'H2992': 'to marry a (deceased) brothers widow (yabam)',
'H2993': 'a brother-in-law (yabam)',
'H2994': 'a sister-in-law (Ybemeth)',
'H2995': 'Jabneel (Yabnel)',
'H2996': 'a building (Yabneh)',
'H2997': 'built of Jah (Yibnyah)',
'H2998': 'building of Jah (Yibniyah)',
'H2999': 'pouring forth (Yabboq)',
'H3000': 'Jeberekjah (Yberekyahuw)',
'H3001': 'to be ashamed, confused or disappointed (yaw-bashe)',
'H3002': 'dry (yaw-bashe)',
'H3003': 'Jobesh, the name of an Israelite and of a place in Israel (yaw-bashe)',
'H3004': 'dry ground (yab-baw-shaw)',
'H3005': 'fragrant (yib-sawm)',
'H3006': 'dry ground (yab-beh-sheth)',
'H3008': 'avenger (yig-awl)',
'H3009': 'to dig or plow (yaw-gab)',
'H3010': 'a plowed field (yaw-gabe)',
'H3011': 'hillock (yog-beh-haw)',
'H3012': 'magnified of Jah (yig-dal-yaw-hoo)',
'H3013': 'to grieve (yaw-gaw)',
'H3014': 'to push away (yaw-gaw)',
'H3015': 'affliction (yaw-gohn)',
'H3016': 'fearful (yaw-gore)',
'H3017': 'a lodging (yaw-goor)',
'H3018': 'toil (yeg-ee-ah)',
'H3019': 'tired (yaw-ghee-ah)',
'H3020': 'exiled (yog-lee)',
'H3021': '(properly) to gasp (yaw-gah)',
'H3022': 'earnings (as the product of toil) (yaw-gaw)',
'H3023': 'tired (yaw-gay-ah)',
'H3024': 'fatigue (yeg-ee-aw)',
'H3025': 'to fear (yaw-gore)',
'H3027': 'a hand (the open one (indicating power, means, direction, etc.), in distinction from H3709, the closed one) (yawd)',
'H3030': 'Jidalah, a place in Israel (yid-al-aw)',
'H3031': 'perhaps honeyed (yid-bawsh)',
'H3032': '(properly) to handle, i.e. to throw, e.g. lots (yaw-dad)',
'H3033': '(properly) affection (yed-ee-dooth)',
'H3034': '(literally) to use (i.e. hold out) the hand (yaw-daw)',
'H3035': 'praised (yid-do)',
'H3036': 'thankful (yaw-done)',
'H3037': 'knowing (yad-doo-ah)',
'H3038': 'laudatory (yed-oo-thoon)',
'H3039': 'loved (yed-eed)',
'H3040': 'beloved (yed-ee-daw)',
'H3041': 'beloved of Jah (yed-ee-deh-yaw)',
'H3042': 'praised of Jah (yed-aw-yaw)',
'H3043': 'knowing God (yed-ee-ah-ale)',
'H3044': 'tearful (yid-lawf)',
'H3045': 'to know (yaw-dah)',
'H3047': 'knowing (yaw-daw)',
'H3048': 'Jah has known (yed-ah-yaw)',
'H3049': '(properly) a knowing one (yid-deh-o-nee)',
'H3050': 'Jah, the sacred name (yaw)',
'H3051': '(literally or figuratively) to give (yaw-hab)',
'H3053': '(properly) what is given (by Providence), i.e. a lot (ye-hawb)',
'H3054': 'to Judaize, i.e. become Jewish (yaw-had)',
'H3055': 'Jehud, a place in Israel (yeh-hood)',
'H3056': 'Judaistic (yeh-dah-ee)',
'H3057': 'Jehudijah, a Jewess (yeh-hoo-dee-yaw)',
'H3058': 'Jehovah (is) He (yay-hoo)',
'H3059': 'Jehovah-seized (yeh-ho-aw-khawz)',
'H3060': 'Jehovah-fired (yeh-ho-awsh)',
'H3063': 'celebrated (yeh-hoo-daw)',
'H3064': 'a Jehudite (i.e. Judaite or Jew), or descendant of Jehudah (i.e. Judah) (yeh-hoo-dee)',
'H3065': 'Jehudi, an Israelite (yeh-hoo-dee)',
'H3066': 'the Jewish (used adverbially) language (yeh-hoo-deeth)',
'H3067': 'Jewess (yeh-ho-deeth)',
'H3068': '(the) self-Existent or Eternal (yeh-ho-vaw)',
'H3069': 'God (yeh-ho-vee)',
'H3070': 'Jehovah will see (to it) (yeh-ho-vaw)',
'H3071': 'Jehovah (is) my banner (yeh-ho-vaw)',
'H3072': 'Jehovah (is) our right (ye-ho-vaw)',
'H3073': 'Jehovah (is) peace (yeh-ho-vaw)',
'H3074': 'Jehovah (is) thither (yeh-ho-vaw)',
'H3075': 'Jehovah-endowed (yeh-ho-zaw-bawd)',
'H3076': 'Jehovah-favored (yeh-ho-khaw-nawn)',
'H3077': 'Jehovah-known (yeh-ho-yaw-daw)',
'H3078': 'Jehovah will establish (yeh-ho-yaw-keen)',
'H3079': 'Jehovah will raise (yeh-ho-yaw-keem)',
'H3080': 'Jehovah will contend (yeh-ho-yaw-reeb)',
'H3081': 'potent (yeh-hoo-kal)',
'H3082': 'Jehovah-largessed (yeh-ho-naw-dawb)',
'H3083': 'Jehovah-given (yeh-ho-naw-thawn)',
'H3084': 'Jehoseph (i.e. Joseph), a son of Jacob (yeh-ho-safe)',
'H3085': 'Jehovah-adorned (yeh-ho-ad-daw)',
'H3086': 'Jehovah-pleased (yeh-ho-ad-deen)',
'H3087': 'Jehovah-righted (yeh-ho-tsaw-dawk)',
'H3088': 'Jehovah-raised (yeh-ho-rawm)',
'H3089': 'Jehovah-sworn (yeh-ho-sheh-bah)',
'H3090': 'Jehoshabath, an Israelitess (yeh-ho-shab-ath)',
'H3091': 'Jehovah-saved (yeh-ho-shoo-ah)',
'H3092': 'Jehovah-judged (yeh-ho-shaw-fawt)',
'H3093': 'elated (yaw-here)',
'H3094': 'praising God (yeh-hal-lel-ale)',
'H3095': 'a precious stone, probably onyx (yah-hal-ome)',
'H3096': 'perhaps threshing-floor (yah-hats)',
'H3097': 'Jehovah-fathered (yo-awb)',
'H3098': 'Jehovah-brothered (yo-awkh)',
'H3099': 'Joachaz, the name of two Israelites (yo-aw-khawz)',
'H3100': 'Jehovah (is his) God (yo-ale)',
'H3101': 'Joash, the name of six Israelites (yo-awsh)',
'H3102': 'Job, an Israelite (yobe)',
'H3103': 'howler (yo-bawb)',
'H3104': 'the blast of a horn (from its continuous sound) (yo-bale)',
'H3105': 'a stream (yoo-bal)',
'H3106': 'stream (yoo-bawl)',
'H3107': 'Jozabad, the name of ten Israelites (yo-zaw-bawd)',
'H3108': 'Jehovah-remembered (yo-zaw-kawr)',
'H3109': 'Jehovah-revived (yo-khaw)',
'H3110': 'Jochanan, the name of nine Israelites (yo-khaw-nawn)',
'H3111': 'Jojada, the name of two Israelites (yo-yaw-daw)',
'H3112': 'Jojakin, an Israelite king (yo-yaw-keen)',
'H3113': 'Jojakim, an Israelite (yo-yaw-keem)',
'H3114': 'Jojarib, the name of four Israelites (yo-yaw-reeb)',
'H3115': 'Jehovah-gloried (yo-keh-bed)',
'H3116': 'Jukal, an Israelite (yoo-kal)',
'H3117': 'a day (as the warm hours), whether literal (from sunrise to sunset, or from one sunset to the next), or figurative (a space of time defined by an associated term), (often used adverb) (yome)',
'H3119': 'daily (yo-mawm)',
'H3120': 'effervescing (i.e. hot and active) (yaw-vawn)',
'H3121': '(properly) dregs (as effervescing) (yaw-ven)',
'H3122': 'Jonadab, the name of an Israelite and of a Rechabite (yo-naw-dawb)',
'H3123': 'a dove (apparently from the warmth of their mating) (yo-naw)',
'H3124': 'Jonah, an Israelite (yo-naw)',
'H3125': 'a Jevanite, or descendant of Javan (yev-aw-nee)',
'H3126': 'a sucker (yo-nake)',
'H3127': 'a sprout (yo-neh-keth)',
'H3128': 'silent dove of distant places (yo-nath)',
'H3129': 'Jonathan, the name of ten Israelites (yo-naw-thawn)',
'H3130': 'let him add (or perhaps simply active participle adding) (yo-safe)',
'H3131': 'Jah (is) adding (yo-sif-yaw)',
'H3132': 'furthermore (yo-ay-law)',
'H3133': 'appointer (yo-ade)',
'H3134': 'Jehovah (is his) help (yo-eh-zer)',
'H3135': 'Jehovah-hastened (yo-awsh)',
'H3136': 'Jotsadak, an Israelite (yo-tsaw-dawk)',
'H3137': 'Jokim, an Israelite (yo-keem)',
'H3138': 'sprinkling (yo-reh)',
'H3139': 'rainy (yo-raw)',
'H3140': 'rainy (yo-rah-ee)',
'H3141': 'Joram, the name of three Israelites and one Syrian (yo-rawm)',
'H3142': 'kindness will be returned (yoo-shab)',
'H3143': 'Jehovah will cause to dwell (yo-shi-yaw)',
'H3144': 'Joshah, an Israelite (yo-shaw)',
'H3145': 'Jehovah-set (yo-shav-yaw)',
'H3146': 'Joshaphat, an Israelite (yo-shaw-fawt)',
'H3147': 'Jehovah (is) perfect (yo-thawm)',
'H3148': '(properly) redundant (yo-thare)',
'H3149': 'sprinkled of God (yez-av-ale)',
'H3150': 'sprinkled of Jah (yiz-zee-yaw)',
'H3151': 'he will make prominent (yaw-zeez)',
'H3152': 'he will draw out (yiz-lee-aw)',
'H3153': 'Jezanjah, an Israelite (yez-an-yaw)',
'H3154': 'sweat (yeh-zah)',
'H3155': 'a Jizrach (i.e. Ezrachite or Zarchite) or descendant of Zerach (yiz-rawkh)',
'H3156': 'Jah will shine (yiz-rakh-yaw)',
'H3157': 'God will sow (yiz-reh-ale)',
'H3158': 'a Jizreelite or native of Jizreel (yiz-reh-ay-lee)',
'H3159': 'a Jezreelitess (yiz-reh-ay-leeth)',
'H3160': 'hidden (yekh-oob-baw)',
'H3161': 'to be (or become) one (yaw-khad)',
'H3162': '(properly) a unit, i.e. (adverb) unitedly (yakh-ad)',
'H3163': 'his unity, i.e. (adverb) together (yakh-doe)',
'H3164': 'unity of God (yakh-dee-ale)',
'H3165': 'unity of Jah (yekh-dee-yaw-hoo)',
'H3166': 'beheld of God (yakh-az-ee-ale)',
'H3167': 'Jah will behold (yakh-zeh-yaw)',
'H3168': 'God will strengthen (yekh-ez-kale)',
'H3169': 'strengthened of Jah (yekh-iz-kee-yaw)',
'H3170': 'perhaps protection (yakh-zay-raw)',
'H3171': 'God will live (yekh-ee-ale)',
'H3172': 'a Jechielite or descendant of Jechiel (yekh-ee-ay-lee)',
'H3173': '(properly) united, i.e. sole (yaw-kheed)',
'H3174': 'Jah will live (yekh-ee-yaw)',
'H3175': 'expectant (yaw-kheel)',
'H3176': 'to wait (yaw-chal)',
'H3177': 'expectant of God (yakh-leh-ale)',
'H3178': 'a Jachleelite or descendant of Jachleel (yakh-leh-ay-lee)',
'H3179': 'probably to be hot (yaw-kham)',
'H3180': 'a kind of deer (from the color (yakh-moor)',
'H3181': 'hot (yakh-mah-ee)',
'H3182': 'unsandalled (yaw-khafe)',
'H3183': 'God will allot (yakh-tseh-ale)',
'H3184': 'a Jachtseelite (collectively) or descendants of Jachtseel (yakh-tseh-ay-lee)',
'H3185': 'allotted of God (yakh-tsee-ale)',
'H3186': 'to delay (yaw-khar)',
'H3187': 'to enroll by pedigree (yaw-khas)',
'H3188': 'a pedigree or family list (as growing spontaneously) (yakh-as)',
'H3189': 'unity (yakh-ath)',
'H3190': 'to be (causative) make well, literally (sound, beautiful) or figuratively (happy, successful, right) (yaw-tab)',
'H3192': 'pleasantness (yot-baw)',
'H3193': 'Jotbathah, a place in the Desert (yot-baw-thaw)',
'H3194': 'extended (yoo-taw)',
'H3195': 'encircled (i.e. inclosed) (yet-oor)',
'H3196': 'wine (as fermented) (yah-yin)',
'H3197': 'a hand or side (yak)',
'H3198': 'to be right (i.e. correct) (yaw-kahh)',
'H3199': 'he (or it) will establish (yaw-keen)',
'H3200': 'a Jakinite (collectively) or descendants of Jakin (yaw-kee-nee)',
'H3201': 'to be able (yaw-kole)',
'H3203': 'Jah will enable (yek-ol-yaw)',
'H3204': 'Jah will establish (yek-on-yaw)',
'H3205': 'to bear young (yaw-lad)',
'H3206': 'something born, i.e. a lad or offspring (yeh-led)',
'H3207': 'a lass (yal-daw)',
'H3208': 'boyhood (or girlhood) (yal-dooth)',
'H3209': 'born (yil-lode)',
'H3210': 'lodging (yaw-lone)',
'H3211': 'born (yaw-leed)',
'H3212': '(literally or figuratively) to walk (yaw-lak)',
'H3213': 'to howl (with a wailing tone) or yell (with a boisterous one) (yaw-lal)',
'H3214': 'a howl (yel-ale)',
'H3215': 'a howl (yel-aw-law)',
'H3216': 'to blurt or utter inconsiderately (yaw-lah)',
'H3217': 'scurf or tetter (yal-leh-feth)',
'H3218': 'a devourer (yeh-lek)',
'H3219': 'a travelling pouch (as if for gleanings) (yal-koot)',
'H3220': 'a sea (as breaking in noisy surf) or large body of water (yawm)',
'H3222': 'a warm spring (yame)',
'H3223': 'day of God (yem-oo-ale)',
'H3224': '(properly) warm, i.e. affectionate (yem-ee-maw)',
'H3225': 'the right hand or side (leg, eye) of a person or other object (as the stronger and more dexterous) (yaw-meen)',
'H3226': 'Jamin, the name of three Israelites (yaw-meen)',
'H3227': 'right (yem-ee-nee)',
'H3228': 'a Jeminite (collectively) or descendants of Jamin (yem-ee-nee)',
'H3229': 'full (yeem-law)',
'H3230': 'he will make king (yam-lake)',
'H3231': 'to be (physically) right (i.e. firm) (yaw-man)',
'H3232': 'prosperity (as betokened by the right hand) (yim-naw)',
'H3233': 'right (i.e. at the right hand) (yem-aw-nee)',
'H3234': 'he will restrain (yim-naw)',
'H3235': 'to exchange (yaw-mar)',
'H3236': 'interchange (yim-raw)',
'H3237': 'to touch (yaw-mash)',
'H3238': 'to rage or be violent (yaw-naw)',
'H3239': 'quiet (yaw-no-akh;)',
'H3240': 'to deposit (yaw-nakh)',
'H3241': 'asleep (yaw-neem)',
'H3242': 'a sucker or sapling (yen-ee-kaw)',
'H3243': 'to suck (yaw-nak)',
'H3244': 'an unclean (acquatic) bird (yan-shoof)',
'H3245': 'to set (literally or figuratively) (yaw-sad)',
'H3246': 'a foundation (yes-ood)',
'H3247': 'a foundation (literally or figuratively) (yes-ode)',
'H3248': 'a foundation (yes-oo-daw)',
'H3249': 'departing (yaw-soor)',
'H3250': 'a reprover (yis-sore)',
'H3251': 'to pour (intransitive) (yaw-sak)',
'H3252': 'observant (yis-kaw)',
'H3253': 'Jah will sustain (yis-mak-yaw-hoo)',
'H3254': 'to add or augment (often adverbial, to continue to do a thing) (yaw-saf)',
'H3256': 'to chastise, literally (with blows) or figuratively (with words) (yaw-sar)',
'H3257': 'a shovel (yaw)',
'H3258': 'sorrowful (yah-bates)',
'H3259': 'to fix upon (by agreement or appointment) (yaw-ad)',
'H3260': 'appointed (yed-ee)',
'H3261': 'apparently to brush aside (yaw-aw)',
'H3262': 'carried away of God (yeh-oo-ale)',
'H3263': 'counsellor (yeh-oots)',
'H3264': 'a forest (yaw-ore)',
'H3265': 'wooded (yaw-oor)',
'H3266': 'hasty (yeh-oosh)',
'H3267': 'to be bold or obstinate (yaw-az)',
'H3268': 'emboldened of God (yah-az-ee-ale)',
'H3269': 'emboldened of Jah (yah-az-ee-yaw-hoo)',
'H3270': 'helpful (yah-az-ayr)',
'H3271': 'to clothe (yaw-at)',
'H3273': 'carried away of God (yeh-ee-ale)',
'H3274': 'hasty (yeh-eesh)',
'H3275': 'troublesome (yah-kawn)',
'H3276': '(properly) to ascend (yaw-al)',
'H3277': 'an ibex (as climbing) (yaw-ale)',
'H3278': 'Jael, a Canaanite (yaw-ale)',
'H3279': 'Jaala or Jaalah, one of the Nethinim (yah-al-aw)',
'H3280': 'roe (yah-al-aw)',
'H3281': 'occult (yah-lawm)',
'H3282': '(properly, but not used) to heed (yah-an)',
'H3283': 'the ostrich, a ceremonially unclean animal (probably named from its answering cry) (yaw-ane)',
'H3284': 'an unclean bird, the owl or the ostrich (yah-an-aw)',
'H3285': 'responsive (yah-an-ahee)',
'H3286': 'to tire (as if from wearisome flight) (yaw-af)',
'H3287': 'fatigued (yaw-afe;)',
'H3288': 'fatigue (yeh-awf)',
'H3289': 'to advise (yaw-ats)',
'H3290': 'heel-catcher (i.e. supplanter) (yah-ak-obe)',
'H3291': 'Jaakobah, an Israelite (yah-ak-o-baw)',
'H3292': 'Jaakan, an Idumaean (yah-ak-awn)',
'H3293': 'a copse of bushes (yah-ar)',
'H3294': 'Jarah, an Israelite (yah-raw)',
'H3295': '(honey-) comb, forest (yah-ar-aw)',
'H3296': 'woods of weavers (yah-ar-ay)',
'H3297': 'forests (yeh-aw-reem)',
'H3298': 'Jaareshjah, an Israelite (yah-ar-esh-yaw)',
'H3299': 'they will do (yah-as-oo)',
'H3300': 'made of God (yah-as-ee-ale)',
'H3301': 'Jah will liberate (yif-deh-yaw)',
'H3302': '(properly) to be bright (yaw-faw)',
'H3303': 'beautiful (literally or figuratively) (yaw-feh)',
'H3304': 'very beautiful (yef-eh)',
'H3305': 'beautiful (yaw-fo)',
'H3306': '(properly) to breathe hard (yaw-fakh)',
'H3307': '(properly) puffing, i.e. (figuratively) meditating (yaw-fay-akh)',
'H3308': 'beauty (yof-ee)',
'H3309': 'bright (yaw-fee-ah)',
'H3310': 'he will deliver (yaf-late)',
'H3311': 'a Japhletite or descendant of Japhlet (yaf-lay-tee)',
'H3312': 'he will be prepared (yef-oon-neh)',
'H3313': 'to shine (yaw-fah)',
'H3314': 'splendor (yif-aw)',
'H3315': 'expansion (yeh-feth)',
'H3316': 'he will open (yif-tawkh)',
'H3317': 'God will open (yif-tach-ale)',
'H3318': 'to go out (yaw-tsaw)',
'H3320': 'to place (any thing so as to stay) (yaw-tsab)',
'H3322': 'to place permanently (yaw-tsag)',
'H3323': 'oil (as producing light) (yits-hawr)',
'H3324': 'Jitshar, an Israelite (yits-hawr)',
'H3325': 'a Jitsharite or descendant of Jitshar (yits-haw-ree)',
'H3326': 'spread, i.e. a bed (yaw-tsoo-ah)',
'H3327': 'laughter (i.e. mockery) (yits-khawk)',
'H3328': 'he will shine (yits-khar)',
'H3329': 'issue, i.e. offspring (yaw-tsee)',
'H3331': 'to strew as a surface (yaw-tsah)',
'H3332': '(properly) to pour out (transitive or intransitive) (yaw-tsak)',
'H3333': 'poured out, i.e. run into a mould (yets-oo-kaw)',
'H3334': 'to press (intransitive), i.e. be narrow (yaw-tsar)',
'H3335': 'to mould into a form (yaw-tsar)',
'H3336': 'a form (yay-tser)',
'H3337': 'Jetser, an Israelite (yay-tser)',
'H3338': 'structure, i.e. limb or part (yaw-tsoor)',
'H3339': 'formative (yits-ree)',
'H3340': 'a Jitsrite (collectively) or descendants of Jetser (yits-ree)',
'H3341': 'to burn or set on fire (yaw-tsath)',
'H3342': 'a trough (as dug out) (yeh-keb)',
'H3343': 'God will gather (yek-ab-tseh-ale)',
'H3344': 'to burn (yaw-kad)',
'H3347': 'burning of (the) people (yok-deh-awm)',
'H3348': 'obedient (yaw-keh)',
'H3349': 'obedience (yik-kaw-haw)',
'H3350': 'a burning (yek-ode)',
'H3351': '(properly) standing (extant) (yek-oom)',
'H3352': '(properly) entangling (yaw-koshe)',
'H3353': '(properly) entangled (yaw-koosh)',
'H3354': 'obedience of God (yek-ooth-ee-ale)',
'H3355': 'he will be made little (yok-tawn)',
'H3356': 'he will raise (yaw-keem)',
'H3357': 'precious (yak-keer)',
'H3359': 'Jah will rise (yek-am-yaw)',
'H3360': '(the) people will rise (yek-am-awm)',
'H3361': '(the) people will be raised (yok-meh-awm)',
'H3362': '(the) people will be lamented (yok-neh-awm)',
'H3363': '(properly) to sever oneself (yaw-kah)',
'H3364': 'to awake (intransitive) (yaw-kats)',
'H3365': '(properly) apparently, to be heavy, i.e. (figuratively) valuable (yaw-kar)',
'H3366': 'value (yek-awr)',
'H3368': 'valuable (yaw-kawr)',
'H3369': 'to ensnare (literally or figuratively) (yaw-koshe)',
'H3370': 'insidious (yok-shawn)',
'H3371': 'veneration of God (yok-theh-ale)',
'H3372': 'to fear (yaw-ray)',
'H3373': 'fearing (yaw-ray)',
'H3374': 'fear (also used as infinitive) (yir-aw)',
'H3375': 'fearfulness (yir-ohn)',
'H3376': 'fearful of Jah (yir-ee-yaw)',
'H3377': 'he will contend (yaw-rabe)',
'H3378': 'Baal will contend (yer-oob-bah-al)',
'H3379': '(the) people will contend (yaw-rob-awm)',
'H3380': 'shame (i.e. the idol) will contend (yer-oob-beh-sheth)',
'H3381': 'to descend (yaw-rad)',
'H3382': 'a descent (yeh-red)',
'H3383': 'a descender (yar-dane)',
'H3384': '(properly) to flow as water (yaw-raw)',
'H3385': 'founded of God (yer-oo-ale)',
'H3386': '(born at the) new moon (yaw-ro-akh)',
'H3387': 'green, i.e. an herb (yaw-roke)',
'H3388': 'possessed (yer-oo-shaw)',
'H3389': 'founded peaceful (yer-oo-shaw-lah-im)',
'H3391': 'a lunation, i.e. month (yeh-rakh)',
'H3392': 'Jerach, an Arabian patriarch (yeh-rakh)',
'H3394': 'the moon (yaw-ray-akh)',
'H3395': 'compassionate (yer-o-khawm)',
'H3396': 'God will compassionate (yer-akh-meh-ale)',
'H3397': 'a Jerachmeelite or descendant of Jerachmeel (yer-akh-meh-ay-lee)',
'H3398': 'Jarcha, an Egyptian (yar-khaw)',
'H3399': 'to precipitate or hurl (rush) headlong (yaw-rat)',
'H3400': 'thrown of God (yer-ee-ale)',
'H3401': '(literally) he will contend (yaw-rebe)',
'H3402': 'Jarib, the name of three Israelites (yaw-rebe)',
'H3403': 'contentious (yer-eeb-ahee)',
'H3404': 'Jah will throw (yer-ee-yaw)',
'H3405': 'fragrant (yer-ee-kho)',
'H3406': 'elevations (yer-ee-mohth)',
'H3407': 'a hanging (as tremulous) (yer-ee-aw)',
'H3408': 'curtains (yer-ee-ohth)',
'H3409': 'the thigh (from its fleshy softness) (yaw-rake)',
'H3411': '(properly) the flank (yer-ay-kaw)',
'H3412': 'elevation (yar-mooth)',
'H3413': 'elevated (yer-ay-mah-ee)',
'H3414': 'Jah will rise (yir-meh-yaw)',
'H3415': '(properly) to be broken up (with any violent action) i.e. (figuratively) to fear (yaw-rah)',
'H3416': 'God will heal (yir-peh-ale)',
'H3417': 'to spit (yaw-rak)',
'H3418': '(properly) pallor (yeh-rek)',
'H3419': '(properly) green (yaw-rawk)',
'H3420': 'paleness, whether of persons (from fright), or of plants (from drought) (yay-raw-kone)',
'H3421': 'people will be poured forth (yor-keh-awm)',
'H3422': 'yellowishness (yer-ak-rak)',
'H3423': 'to occupy (by driving out previous tenants, and possessing in their place) (yaw-rash)',
'H3424': 'occupancy (yer-ay-shaw)',
'H3425': 'something occupied (yer-oosh-shaw)',
'H3426': 'entity (yaysh)',
'H3427': '(properly) to sit down (specifically as judge. in ambush, in quiet) (yaw-shab)',
'H3428': 'seat of (his) father (yeh-sheb-awb)',
'H3429': 'sitting in the seat (yo-shabe)',
'H3430': 'his dwelling (is) in Nob (yish-bobeh-nobe)',
'H3431': 'he will praise (yish-bakh)',
'H3432': 'a Jashubite, or descendant of Jashub (yaw-shoo-bee)',
'H3433': 'returner of bread (yaw-shoo-bee)',
'H3434': 'people will return (yaw-shob-awm)',
'H3435': 'he will leave (yish-bawk)',
'H3436': 'a hard seat (yosh-bek-aw-shaw)',
'H3437': 'he will return (yaw-shoob)',
'H3438': 'he will level (yish-vaw)',
'H3439': 'Jah will empty (yesh-o-khaw-yaw)',
'H3440': 'level (yish-vee)',
'H3441': 'a Jishvite (collectively) or descendants of Jishvi (yish-vee)',
'H3442': 'he will save (yay-shoo-ah)',
'H3444': 'something saved, i.e. (abstractly) deliverance (yesh-oo-aw)',
'H3445': 'hunger (yeh-shakh)',
'H3446': 'he will laugh (yis-khawk)',
'H3447': 'to extend (yaw-shat)',
'H3448': 'extant (yee-shah-ee)',
'H3449': 'Jah will lend (yish-shee-yaw)',
'H3450': 'God will place (yes-eem-aw-ale)',
'H3451': 'desolation (yesh-ee-maw)',
'H3452': 'a desolation (yesh-ee-mone)',
'H3453': 'an old man (yaw-sheesh)',
'H3454': 'aged (yesh-ee-shah-ee)',
'H3455': 'to place (yaw-sam)',
'H3456': 'to lie waste (yaw-sham)',
'H3457': 'desolate (yish-maw)',
'H3458': 'God will hear (yish-maw-ale)',
'H3459': 'a Jishmaelite or descendant of Jishmael (yish-maw-ay-lee)',
'H3460': 'Jah will hear (yish-mah-yaw)',
'H3461': 'preservative (yish-mer-ah-ee)',
'H3462': '(properly) to be slack or languid (yaw-shane)',
'H3463': 'sleepy (yaw-shane)',
'H3464': 'Jashen, an Israelite (yaw-shane)',
'H3465': 'old (yaw-shawn)',
'H3466': 'Jeshanah, a place in Israel (yesh-aw-naw)',
'H3467': '(properly) to be open, wide or free (yaw-shah)',
'H3468': 'liberty, deliverance, prosperity (yeh-shah)',
'H3469': 'saving (yish-ee)',
'H3470': 'Jah has saved (yesh-ah-yaw)',
'H3471': 'a gem supposed to be jasper (from the resemblance in name) (yaw-shef-ay)',
'H3472': 'he will scratch (yish-paw)',
'H3473': 'he will hide (yish-pawn)',
'H3474': 'to be straight or even (yaw-shar)',
'H3475': 'the right (yay-sher)',
'H3476': 'the right (yo-sher)',
'H3477': 'straight (yaw-shawr)',
'H3478': 'he will rule as God (yis-raw-ale)',
'H3480': 'right towards God (yes-ar-ale-aw)',
'H3481': 'a Jisreelite or descendant of Jisrael (yis-reh-ay-lee)',
'H3482': 'a Jisreelitess or female descendant of Jisrael (yis-reh-ay-leeth)',
'H3483': 'rectitude (yish-raw)',
'H3484': 'upright (yesh-oo-roon)',
'H3485': 'he will bring a reward (yis-saw-kawr)',
'H3486': 'gray-haired, i.e. an aged man (yaw-shaysh)',
'H3489': 'a peg (yaw-thade)',
'H3490': 'a bereaved person (yaw-thome)',
'H3491': '(properly) what is left (yaw-thoor)',
'H3492': 'redundant (yat-teer)',
'H3494': 'it will hang, i.e. be high (yith-law)',
'H3495': 'orphanage (yith-maw)',
'H3496': 'continued of God (yath-nee-ale)',
'H3497': 'extensive (yith-nawn)',
'H3498': 'to jut over or exceed (yaw-thar)',
'H3499': '(properly) an overhanging (yeh-ther)',
'H3501': 'preeminence (yithrah)',
'H3502': 'Jithream (Yithream)',
'H3503': 'an Ithrite (Yithriy)',
'H3504': 'Jithro (Yithrow)',
'H3505': 'Jether (Yether)',
'H3506': 'Jether (Yether)',
'H3507': 'Jetheth (Yetheth)',
'H3508': 'so (ka)',
'H3509': 'to be pained (kaab)',
'H3510': 'pain (keeb)',
'H3511': 'pain (kob)',
'H3512': 'faint, disheartened (kaah)',
'H3513': 'to be heavy, glorious (kabad)',
'H3514': 'to be heavy, glorious (kabed)',
'H3515': 'heavy (kabed)',
'H3516': 'liver (kabed)',
'H3517': 'heaviness (kobed)',
'H3518': 'weight (kobeduwth)',
'H3519': 'glory, honor (kabowd)',
'H3520': 'something heavy (kabud)',
'H3521': 'heavy (kabiyr)',
'H3522': 'great (kabiyr)',
'H3523': 'a quilt, network (kebiyr)',
'H3524': 'already (kebar)',
'H3525': 'length (kebar)',
'H3526': 'a sieve (kebarah)',
'H3527': 'Kibroth Hattaavah (Kibrowth hatTaavah)',
'H3528': 'Cabul (Kabul)',
'H3529': 'fetter (kebel)',
'H3530': 'to gird, bind (kabar)',
'H3531': 'Kibzaim (Kibtsayim)',
'H3532': 'to tread down (kabas)',
'H3533': 'a footstool (kebesh)',
'H3534': 'a lamb (kebes)',
'H3535': 'a lamb (kabsah)',
'H3536': 'a furnace (kibshan)',
'H3537': 'to subdue (kabash)',
'H3538': 'a pitcher (kad)',
'H3539': 'a small pitcher (kaddowd)',
'H3540': 'a spark (kiydowd)',
'H3541': 'thus, so (kadein)',
'H3542': 'Kedar (Kedar)',
'H3543': 'darkness (kadar)',
'H3544': 'to be dark (kadar)',
'H3545': 'darkness, gloom (kadruwth)',
'H3546': 'so (koh)',
'H3547': 'to be blunt, faint (kahah)',
'H3548': 'faint, dark (kehheh)',
'H3549': 'a healing (kehah)',
'H3550': 'Kohath (Kohath)',
'H3551': 'Kohathite (Kohathiy)',
'H3552': 'a window (kavvah)',
'H3553': 'burning (keviyyah)',
'H3554': 'to be extinguished (kaah)',
'H3555': 'helmet (kowba)',
'H3556': 'a star (kowkab)',
'H3557': 'thus, so (koh)',
'H3558': 'thus (kow)',
'H3559': 'to wait for (kavah)',
'H3560': 'Koa (Kowa)',
'H3561': 'burning (kuwnah)',
'H3562': 'Cun (Kuwn)',
'H3563': 'a cake (kavvan)',
'H3564': 'Cush (Kuwsh)',
'H3565': 'Cushan (Kuwshan)',
'H3566': 'Cushan Rishathaim (Kuwshan Rishathayim)',
'H3567': 'Cushi (Kuwshiy)',
'H3568': 'Ethiopia (Kuwsh)',
'H3569': 'an Ethiopian (Kuwshiy)',
'H3570': 'an Ethiopian woman (Kuwshiyth)',
'H3571': 'Cuth, Cuthah (Kuwth)',
'H3572': 'Cuthite (Kuwthiy)',
'H3573': 'to be removed (kuth)',
'H3574': 'strength (koach)',
'H3575': 'Koz (Kowz)',
'H3576': 'Kozbi (Kozbiy)',
'H3577': 'a lie, falsehood (kazab)',
'H3578': 'Kozeba (Kozeba)',
'H3579': 'a liar (kazzab)',
'H3580': 'to lie (kachad)',
'H3581': 'to hide, conceal (kachad)',
'H3582': 'lean (kachash)',
'H3583': 'leanness (kachash)',
'H3584': 'a lie, deception (kachash)',
'H3585': 'meager, lean (kachash)',
'H3586': 'to deny, deceive (kachash)',
'H3587': 'for, because, that (kiy)',
'H3588': 'that, because (kiy)',
'H3589': 'a brand, burning (kiyd)',
'H3590': 'destruction (kiyd)',
'H3591': 'Orion (Kiyown)',
'H3592': 'a key (kiyowr)',
'H3TwoNineThree': 'a gnat (kayl)',
'H3594': 'a javelin (kiydown)',
'H3595': 'a battle axe (kiymahh)',
'H3596': 'bag (kiys)',
'H3597': 'Kish (Kiysh)',
'H3598': 'Kish (Kiysh)',
'H3599': 'Kishi (Kiyshiy)',
'H3600': 'Kishon (Kiyshown)',
'H3601': 'Kishon (Kiyshown)',
'H3602': 'to ensnare (kakah)',
'H3603': 'like as (kakkemow)',
'H3604': 'thus (kak)',
'H3605': 'all, every, whole (kol)',
'H3606': 'all (kol)',
'H3607': 'Kilab (Kilab)',
'H3608': 'a dog (keleb)',
'H3609': 'Caleb (Kaleb)',
'H3610': 'Caleb Ephrathah (Kaleb Ephrathah)',
'H3611': 'all (kol)',
'H3612': 'Calebite (Kalebiy)',
'H3613': 'a basket (keluwb)',
'H3614': 'Chelubai (Keluwbay)',
'H3615': 'to finish, complete (kalah)',
'H3616': 'to finish (kelah)',
'H3617': 'completion, end (kalah)',
'H3618': 'a bride, daughter-in-law (kallah)',
'H3619': 'destruction (kilayown)',
'H3620': 'two kinds (kilayim)',
'H3621': 'all (kolel)',
'H3622': 'Kelal (Kelal)',
'H3623': 'perfect (kaliyl)',
'H3624': 'something complete, a whole (kaliyl)',
'H3625': 'perfection (kalliy)',
'H3626': 'Kelaiah (Kelayah)',
'H3627': 'vessel, implement, weapon (keliy)',
'H3628': 'a prison (keliy)',
'H3629': 'a prison (kele)',
'H3630': 'kidneys (kilyah)',
'H3631': 'to hold back, restrain (kala)',
'H3632': 'to complete, finish (kalam)',
'H3633': 'Kelmad (Kelmad)',
'H3634': 'to be ashamed (kalam)',
'H3635': 'shame (kelimmah)',
'H3636': 'shame, reproach (kelimmuth)',
'H3637': 'so, thus (ken)',
'H3638': 'Kenan (Kenan)',
'H3639': 'to set upright (kanan)',
'H3640': 'Kenath (Kenath)',
'H3641': 'Kenaz (Kenaz)',
'H3642': 'Kenizzite (Kenizziy)',
'H3643': 'to gather (kanas)',
'H3644': 'to gather (kenas)',
'H3645': 'a collection (keneth)',
'H3646': 'to bow down (kana)',
'H3647': 'Kinnereth (Kinnereth)',
'H3648': 'Kinneroth (Kinnerowth)',
'H3649': 'thus (kan)',
'H3650': 'gnat (kinnim)',
'H3651': 'a base, pedestal (ken)',
'H3652': 'thus (ken)',
'H3653': 'a gnat (ken)',
'H3654': 'companion (kenaah)',
'H3655': 'companion (kenaah)',
'H3656': 'companion (kenath)',
'H3657': 'companion (kenath)',
'H3658': 'a cake (kanniy)',
'H3659': 'Canaan (Kenaan)',
'H3660': 'Canaanite (Kenaaniy)',
'H3661': 'to be humble (kana)',
'H3662': 'Canaanitess (Kenaaniy)',
'H3663': 'humble (kana)',
'H3664': 'humiliation (kanaah)',
'H3665': 'to cover (kanaph)',
'H3666': 'Canaan (Kenaan)',
'H3667': 'Canaanite (Kenaaniy)',
'H3668': 'Canaanitish (Kenaaniy)',
'H3669': 'wing, skirt (kanaph)',
'H3670': 'a wing (kanaph)',
'H3LetMeSevenOne': 'to give a name, title (kanah)',
'H3672': 'Coniah (Konyahuw)',
'H3673': 'Keni (Qeniy)',
'H3674': 'Kenite (Qeniy)',
'H3675': 'Kenizzite (Qenizziy)',
'H3676': 'to surround (kanas)',
'H3677': 'a harp (kinnowr)',
'H3678': 'a chair, throne (kisse)',
'H3679': 'a covering (kecuwy)',
'H3680': 'to cover (kasah)',
'H3681': 'to cover (kasah)',
'H3682': 'a covering (kesuwth)',
'H3683': 'Kislon (Kislown)',
'H3684': 'confidence, folly (kesel)',
'H3685': 'loin (kesel)',
'H3686': 'folly (kesil)',
'H3687': 'Orion (Kesiyl)',
'H3688': 'to be foolish (kasal)',
'H3689': 'Kislev (Kislev)',
'H3690': 'confidence (kislah)',
'H3691': 'Chesil (Kesiyl)',
'H3692': 'to cut off (kasach)',
'H3693': 'spelt (kussemeth)',
'H3694': 'spelt (kussmim)',
'H3695': 'to count, reckon (kasas)',
'H3696': 'a cushion (keseth)',
'H3697': 'Kisloth Tabor (Kisloth Tabowr)',
'H3698': 'to long for (kasaph)',
'H3699': 'longing (kesoph)',
'H3700': 'to be pale (kasaph)',
'H3701': 'silver, money (keseph)',
'H3702': 'silver (kesaph)',
'H3703': 'a chair (kisse)',
'H3704': 'a covering (keseh)',
'H3705': 'full moon (kese)',
'H3706': 'Chesed (Kesed)',
'H3707': 'Casiphia (Kasiphya)',
'H3708': 'to cut down (kasam)',
'H3709': 'now (kaeth)',
'H3710': 'now (kaen)',
'H3711': 'now (kaeth)',
'H3712': 'to crush (kaphaph)',
'H3713': 'to urge (kaphaph)',
'H3714': 'rock (keph)',
'H3715': 'a rock (keph)',
'H3716': 'a spoon, palm, sole (kaph)',
'H3717': 'a rock (kephiyr)',
'H3718': 'a village (kaphar)',
'H3719': 'a village (kephar)',
'H3720': 'Chephirah (Kephiyrah)',
'H3721': 'a young lion (kephiyr)',
'H3722': 'to cover, make atonement (kaphar)',
'H3723': 'a village (kaphar)',
'H3724': 'pitch, cypress (kopher)',
'H3725': 'atonement (kippur)',
'H3726': 'frost (kephowr)',
'H3727': 'a bowl (kaphown)',
'H3728': 'a cover (kapporeth)',
'H3729': 'Chephar-ammoni (Kephar haAmmowniy)',
'H3730': 'a vessel (kar)',
'H3731': 'a pasture (kar)',
'H3732': 'a cor (kor)',
'H3733': 'a mule (kirkarah)',
'H3734': 'Karkor (Karkor)',
'H3735': 'to dig (karah)',
'H3736': 'a digging (karah)',
'H3737': 'a pasture (kerah)',
'H3738': 'to cover (karah)',
'H3739': 'a meal (karah)',
'H3740': 'Cherub (Keruwb)',
'H3741': 'Cherub (Keruwb)',
'H3742': 'a cherub (keruwb)',
'H3743': 'Cheran (Keran)',
'H3744': 'saffron (karkom)',
'H3745': 'Carchemish (Karkemiysh)',
'H3746': 'a vineyard (kerem)',
'H3747': 'Carmel (Karmel)',
'H3748': 'Carmel (Karmel)',
'H3749': 'Carmelite (Karmliy)',
'H3750': 'Carmelitess (Karmliyth)',
'H3751': 'garden land (karmel)',
'H3752': 'Kerioth (Keriyowth)',
'H3753': 'Kerioth (Keriyowth)',
'H3754': 'a beam (keruthah)',
'H3755': 'Cherith (Keriyth)',
'H3756': 'Cherethite (Kerethiy)',
'H3757': 'Carkas (Karkas)',
'H3758': 'a lamb (kar)',
'H3759': 'a lamb (karah)',
'H3760': 'to bend, bow (kara)',
'H3761': 'a throne (korse)',
'H3762': 'legs (kara)',
'H3763': 'a camel (kirkarah)',
'H3764': 'to dance (karar)',
'H3765': 'Koresh (Koresh)',
'H3766': 'Cyrus (Koresh)',
'H3767': 'to cut off (karath)',
'H3768': 'to cut off (kerath)',
'H3Note769': 'beams (keruthoth)',
'H3770': 'Cherethites (Kerethiy)',
'H3771': 'Cherethites (Kerethiy)',
'H3772': 'a cutting off (karath)',
'H3773': 'Kesil (Kesil)',
'H3774': 'to write (kathab)',
'H3775': 'to write (kethab)',
'H3776': 'a writing (kethab)',
'H3777': 'a writing (kethab)',
'H3778': 'Kittim (Kittim)',
'H3779': 'a writing (kethobeth)',
'H3Details80': 'a wall (kothel)',
'H3781': 'to pound, crush (kathath)',
'H3782': 'to write (kathab)',
'H3783': 'shoulder (katheph)',
'H3784': 'Kithlish (Kithliysh)',
'H3785': 'linen (kethoneth)',
'H3786': 'a wall (kothal)',
'H3787': 'to surround (kathar)',
'H3788': 'a capital (kothereth)',
'H3789': 'to be crushed (katha)',
'H3790': 'to crush (kathash)',
'H3791': 'to write (kthab)',
'H3792': 'writing (kthab)',
'H3793': 'writing (kthab)',
'H3794': 'Kittim (Kittiy)',
'H3795': 'Kittim (Kittiy)',
'H3796': 'a tunic (kuttineth)',
'H3797': 'crushed (katheth)',
'H3798': 'to (le)',
'H3799': 'to (le)',
'H3800': 'not (lo)',
'H3801': 'to him, for him (loh)',
'H3802': 'to be weary (laah)',
'H3803': 'to weary (laah)',
'H3804': 'weariness (leah)',
'H3805': 'Leah (Leah)',
'H3806': 'not (la)',
'H3807': 'not (la)',
'H3808': 'not, no (lo)',
'H3809': 'not (lo)',
'H3810': 'Lodebar (Lo Debar)',
'H3811': 'weariness (telaah)',
'H3812': 'Leban (Laban)',
'H3813': 'Laban (Laban)',
'H3814': 'to make bricks (laban)',
'H3815': 'Libnah (Libnah)',
'H3816': 'heart (leab)',
'H3817': 'heart (libba)',
'H3818': 'heart (leb)',
'H3819': 'heart (leb)',
'H3820': 'heart (leb)',
'H3821': 'heart (lebab)',
'H3822': 'heart (lebab)',
'H3823': 'to take heart (labab)',
'H3824': 'to make cakes (labab)',
'H3Both25': 'a cake (lebibah)',
'H3826': 'Laban (Laban)',
'H3827': 'white (laben)',
'H3828': 'a brick (lebenah)',
'H3829': 'Libnah (Libnah)',
'H3830': 'Libni (Libniy)',
'H3831': 'Libnite (Libniy)',
'H3832': 'Libnah (Libnah)',
'H3Error333': 'storax tree (libneh)',
'H3834': 'poplar (libneh)',
'H3835': 'to be white (laban)',
'H3836': 'Lebanon (Lebanown)',
'H3837': 'frankincense (lebonah)',
'H3838': 'Lebonah (Lebownah)',
'H3839': 'white (laban)',
'H3840': 'moon (lebanah)',
'H3841': 'to clothe (labash)',
'H3842': 'to be white (laban)',
'H3843': 'white (libneh)',
'H3844': 'Lebanon (Lebanown)',
'H3845': 'to clothe (lebash)',
'H3846': 'garment (lebush)',
'H3847': 'garment (lebush)',
'H3848': 'flame (labbah)',
'H3849': 'a flame (labbat)',
'H3850': 'Lebaoth (Lebaowth)',
'H3851': 'a flame (lahab)',
'H3852': 'flame (lahab)',
'H3853': 'a blade, flame (lahab)',
'H3854': 'a flame (lehabah)',
'H3855': 'flaming (lahabah)',
'H3856': 'to burn (lahat)',
'H3857': 'burning (lahat)',
'H3858': 'secret arts (lahat)',
'H3859': 'Lahad (Lahad)',
'H3860': 'Lahmam (Lachmam)',
'H3861': 'to waste away (lahah)',
'H3862': 'they (lahen)',
'H3863': 'they (lahen)',
'H3864': 'except, unless (luw)',
'H3865': 'if (lu)',
'H3866': 'Luz (Luwz)',
'H3867': 'Luz (Luwz)',
'H3868': 'to lodge, remain (luwn)',
'H3869': 'Luz (Luwz)',
'H3870': 'almond (luwz)',
'H3871': 'to turn aside (luwz)',
'H3872': 'perverseness (luwz)',
'H3873': 'Luhith (Luwchiyth)',
'H3874': 'to swallow, swallow down (luwa)',
'H3875': 'Lot (Lowt)',
'H3876': 'Lotan (Lowtan)',
'H3877': 'a covering (lowt)',
'H3TwoEight': 'myrrh (lowt)',
'H3879': 'to join, be joined (lavah)',
'H3880': 'Levi (Leviy)',
'H3881': 'Levi (Leviy)',
'H3882': 'a wreath (livyah)',
'H3883': 'perhaps (luwlay)',
'H3884': 'unless (lule)',
'H3885': 'winding stairs (luwl)',
'H3886': 'to lodge (luwn)',
'H3887': 'to murmur (luwn)',
'H3888': 'a lodging place (luwn)',
'H3889': 'to swallow (luwa)',
'H3890': 'jaw (lechuw)',
'H3891': 'to lick (lachak)',
'H3892': 'to fight (lacham)',
'H3893': 'Lahmi (Lachmiy)',
'H3894': 'to fight (lcham)',
'H3895': 'fresh (lacham)',
'H3896': 'Lehi (Lechiy)',
'H3TwoNineSeven': 'jawbone (lechiy)',
'H3898': 'to fight (lacham)',
'H3899': 'bread, food (lechem)',
'H3900': 'war (lechem)',
'H3901': 'war (lacham)',
'H3902': 'food (lacham)',
'H3903': 'to whisper (lachash)',
'H3904': 'a whispering, charm (lachash)',
'H3905': 'an amulet (lachash)',
'H3906': 'Lahat (Lachat)',
'H3907': 'secretly (lat)',
'H3908': 'a whisper (laash)',
'H3909': 'secretly (lat)',
'H3910': 'an incantation (lat)',
'H3911': 'lizard (letaa)',
'H3912': 'Ladan (Ladan)',
'H3913': 'Lot (Lowt)',
'H3914': 'to hammer, sharpen (latash)',
'H3915': 'night (layil)',
'H3916': 'night (lele)',
'H3917': 'night (layelah)',
'H3918': 'Lilith (liyliyth)',
'H3919': 'Lasha (Lasha)',
'H3920': 'to learn (lamad)',
'H3921': 'Lamech (Lemek)',
'H3922': 'Lamech (Lemek)',
'H3923': 'Lemuel (Lemuwel)',
'H3924': 'Lemuel (Lemuwel)',
'H3925': 'to teach (lamad)',
'H3926': 'taught (limmud)',
'H3927': 'taught (limmud)',
'H3928': 'oxgoad (malmad)',
'H3929': 'Laish (Layish)',
'H3930': 'lion (layish)',
'H3931': 'Laishah (Layishah)',
'H3932': 'Lasha (Lasha)',
'H3933': 'to mock, scorn (latsats)',
'H3934': 'stammering (laeg)',
'H3935': 'a scorner (latsown)',
'H3936': 'stammering (laag)',
'H3937': 'to mock, scorn (laag)',
'H3938': 'to interpret (lats)',
'H3939': 'tongue, language (lashown)',
'H3940': 'tongue (lishshan)',
'H3941': 'to use the tongue (lashan)',
'H3942': 'Lappidoth (Lappiydowth)',
'H3Error943': 'a torch (lappiyd)',
'H3944': 'to fall (lapath)',
'H3945': 'to take (laqach)',
'H3946': 'instruction (leqach)',
'H3947': 'to take, receive (laqach)',
'H3948': 'to take (leqach)',
'H3949': 'tongs (leqach)',
'H3950': 'to gather, glean (laqat)',
'H3951': 'a gleaning (leqet)',
'H3952': 'to lick up (laqaq)',
'H3953': 'Likhi (Liqchiy)',
'H3954': 'late rain (malqowsh)',
'H3955': 'to stammer (laqaq)',
'H3956': 'to slander (lashan)',
'H3957': 'chamber (lishkah)',
'H3958': 'Leshem (Leshem)',
'H3Example959': 'Leshem (Leshem)',
'H3960': 'a chamber (lishkah)',
'H3961': 'tongue (lashown)',
'H3962': 'Lasha (Lasha)',
'H3963': 'moist (leshad)',
'H3964': 'Leshem (Leshem)',
'H3965': 'Letushim (Letuwshim)',
'H3966': 'very (meod)',
'H3967': 'me, I (o)',
'H3968': 'a hundred (meah)',
'H3969': 'a hundred (meah)',
'H3970': 'a hundredth (meah)',
'H3971': 'to refuse, reject (maan)',
'H3972': 'refuse (maen)',
'H3973': 'Meah (Meah)',
'H3974': 'Mibzar (Mibtsar)',
'H3975': 'Mibsam (Mibsam)',
'H3976': 'a choice (mibchar)',
'H3977': 'a choice (mibchowr)',
'H3978': 'a boil (mabow)',
'H3979': 'confidence (mibta)',
'H3980': 'confidence (mibta)',
'H3981': 'a rash utterance (mibta)',
'H3982': 'confusion (mebuwkah)',
'H3983': 'treading down (mebuwsah)',
'H3984': 'to mix, mingle (mabul)',
'H3985': 'a flood (mabbuwl)',
'H3986': 'Me-jarkon (Mey Yarqown)',
'H3987': 'a spring (mabbua)',
'H3988': 'a look (mabbat)',
'H3989': 'a hopeful look (mabbat)',
'H3990': 'to cook (bashal)',
'H3991': 'cooked (mibshalah)',
'H3992': 'glad tidings (mebasser)',
'H3993': 'tidings (mebassereth)',
'H3994': 'shame (mebush)',
'H3995': 'Magbish (Magbiysh)',
'H3996': 'a high place (migbaah)',
'H3997': 'a cap (migbaah)',
'H3Note998': 'a clod (megephah)',
'H3999': 'Magdiel (Magdiyel)',
'H4000': 'a spring, fountain (mabuwa)',
'H4001': 'a particle (mabben)',
'H4002': 'food (migdanah)',
'H4003': 'precious thing, fruit (meged)',
'H4004': 'a lodging place (magor)',
'H4005': 'a lodging place (megurah)',
'H4006': 'fear (megorah)',
'H4007': 'fear (magor)',
'H4008': 'to quiver (magar)',
'H4009': 'a grain pit (megurah)',
'H4010': 'a saw (megerah)',
'H4011': 'Migron (Migron)',
'H4012': 'a clod (megraphah)',
'H4013': 'to cast down, hurl (magar)',
'H4014': 'pasture, open land (migrash)',
'H4015': 'produce (migrashah)',
'H4016': 'a staff (madda)',
'H4017': 'Midian (Midyan)',
'H4018': 'Midianite (Midani)',
'H4019': 'a measure, cloth (mad)',
'H4020': 'a measure (middah)',
'H4021': 'extension (middah)',
'H4022': 'a measure (medad)',
'H4023': 'Medeba (Medeba)',
'H4024': 'a heap (medabah)',
'H4025': 'Madmannah (Madmannah)',
'H44026': 'to measure (madad)',
'H4027': 'stretching (mad)',
'H4028': 'a measured portion (mad)',
'H4029': 'a garment (madveh)',
'H4030': 'a cause of falling (madchepheh)',
'H4031': 'Madon (Madon)',
'H4032': 'a heap (madmen)',
'H4033': 'a dung heap (madmenah)',
'H4034': 'dung (madmen)',
'H4035': 'a measuring instrument (mad)',
'H4036': 'to measure (meda)',
'H4037': 'a measuring (medad)',
'H4038': 'to perceive, know (mada)',
'H4039': 'knowledge (madda)',
'H4040': 'knowledge (manda)',
'H4041': 'why? (maddua)',
'H4042': 'disease (madveh)',
'H4043': 'a kingdom (malkuth)',
'H4044': 'dwelling (medor)',
'H4045': 'a section (medinah)',
'H4046': 'crushing (medichah)',
'H4047': 'strife (midyan)',
'H4048': 'Medan (Medan)',
'H4049': 'a Mede (Maday)',
'H4050': 'Media (Maday)',
'H4051': 'a Mede (Meday)',
'H4052': 'a Mede (Madaah)',
'H4053': 'strife (madon)',
'H4054': 'a thrust (madqar)',
'H4055': 'what (mah)',
'H4056': 'what (meh)',
'H4057': 'what (ma)',
'H4058': 'to delay (mahah)',
'H4059': 'lingering (mihmah)',
'H4060': 'to mix (mahal)',
'H4061': 'to strike, beat (halam)',
'H4062': 'strokes, blows (halumoth)',
'H4063': 'a hammer (halamuth)',
'H4064': 'thither, beyond (haleah)',
'H4065': 'a stroke (mahalummor)',
'H4066': 'to murmur, rage (hamah)',
'H4067': 'abundance (hamon)',
'H4068': 'sound (hemyah)',
'H4069': 'to confuse, discomfit (hamam)',
'H4070': 'Haman (Haman)',
'H4071': 'a storehouse (mamgura)',
'H4H072': 'Ham (Ham)',
'H4073': 'to disturb, drive (hum)',
'H4074': 'to multiply (haman)',
'H4075': 'Hamonah (Hamonah)',
'H4076': 'multitude of Gog (Hamon Gog)',
'H4077': 'a gift (meheman)',
'H4078': 'to change, exchange (mur)',
'H4079': 'brawling (midonim)',
'H4080': 'Midianite (Midiyani)',
'H4081': 'to waver, tremble (mot)',
'H4082': 'a place (medinah)',
'H4083': 'a thrusting (madqarah)',
'H4084': 'what (mah)',
'H4085': 'what (meh)',
'H4086': 'what (ma)',
'H4087': 'what (meh)',
'H4088': 'what (mah)',
'H4089': 'what (man)',
'H4090': 'a part (min)',
'H4091': 'from (min)',
'H4092': 'from (minni)',
'H4093': 'from (min)',
'H4094': 'a string (men)',
'H4095': 'to withhold (mana)',
'H4096': 'a portion (manah)',
'H4097': 'a part (manah)',
'H4098': 'a weight, mina (maneh)',
'H4099': 'a yoke (motah)',
'H4100': 'what (mah)',
'H4101': 'what (meh)',
'H4102': 'what (ma)',
'H4103': 'what (ma)',
'H4104': 'what (meh)',
'H4105': 'what (mah)',
'H4106': 'what (meh)',
'H4107': 'what (mah)',
'H4108': 'what (meh)',
'H4109': 'what (mah)',
'H4110': 'what (mah)',
'H4111': 'Mahalaleel (Mahalalel)',
'H4112': 'praise (mahalal)',
'H4113': 'Mahalath (Machalath)',
'H4114': 'Mahalath (Machalath)',
'H4115': 'disease (machaleh)',
'H4116': 'a blow (mahamorah)',
'H4117': 'Mahanaim (Machanayim)',
'H4118': 'a camp (machaneh)',
'H4119': 'a vision (mechazeh)',
'H4120': 'a window (mechizah)',
'H4121': 'Mahazioth (Machazioth)',
'H4122': 'choice (meche)',
'H4123': 'Makhir (Makir)',
'H4124': 'a price (mechir)',
'H4125': 'sold (mimkar)',
'H4126': 'a sale (meker)',
'H4127': 'Mukhir (Makiri)',
'H4128': 'to sink (makak)',
'H4129': 'a sale (mekerah)',
'H4130': 'a price (machir)',
'H4131': 'a bar (mot)',
'H4132': 'to totter, shake (mot)',
'H4133': 'a shaking (mot)',
'H4134': 'to press, tread down (mashash)',
'H4135': 'to feel (mush)',
'H4136': 'to depart (mush)',
'H4137': 'a lamp (menorah)',
'H4138': 'a grant (man)',
'H4139': 'a portion (minhah)',
'H4140': 'Minnith (Minnith)',
'H4141': 'a stringed instrument (minnim)',
'H4142': 'from (minney)',
'H4143': 'to number, count (manah)',
'H4144': 'a portion (manah)',
'H4145': 'a number (mene)',
'H4146': 'a numbering (mene)',
'H4147': 'to restrain (mana)',
'H4148': 'a lock, bolt (manul)',
'H4149': 'a flight (manos)',
'H4150': 'a refuge (manos)',
'H4151': 'a yoke (motah)',
'H4152': 'a pole (mot)',
'H4153': 'a pole (motah)',
'H4154': 'a gathering place (moed)',
'H4155': 'appointed place (moed)',
'H4156': 'an assembly (moed)',
'H4157': 'to appoint (yaad)',
'H4158': 'an appointed place (moadah)',
'H4159': 'to fly (uph)',
'H4160': 'darkness (muph)',
'H4161': 'to shine (yapha)',
'H4162': 'a striking (mephits)',
'H4163': 'a breathing out (mappach)',
'H4164': 'a fall (mappal)',
'H4165': 'refuse (mappal)',
'H4166': 'a falling (mappalah)',
'H4167': 'a fragment (mappelet)',
'H4168': 'to break (maphats)',
'H4169': 'a hammer (mappets)',
'H4170': 'a shattering (mappats)',
'H4171': 'Mephaath (Mephaath)',
'H4172': 'to expire (puach)',
'H4173': 'a wonder (mopheth)',
'H4174': 'Mappiq (mappiq)',
'H4175': 'a melting (massa)',
'H4176': 'to melt (masas)',
'H4177': 'a melting (mes)',
'H4178': 'a journey (massa)',
'H4179': 'a quarry (massa)',
'H4180': 'a burden (massa)',
'H4181': 'a burden (massa)',
'H4182': 'a burden (massaah)',
'H4183': 'a shooting (masso)',
'H4184': 'a covering (masveh)',
'H4185': 'a removal (masos)',
'H4186': 'to feel (mashash)',
'H4187': 'to depart (mush)',
'H4188': 'to depart (mish)',
'H4189': 'a departure (mush)',
'H4190': 'a departure (mushah)',
'H4191': 'to draw out (mashah)',
'H4192': 'silk (meshi)',
'H4193': 'a pulling (moshekah)',
'H4194': 'to die (muth)',
'H4195': 'a piece (mith)',
'H4196': 'a balance (mozen)',
'H4197': 'a storehouse (mazu)',
'H4198': 'a scattering (mazor)',
'H4199': 'a scattering (mazoreh)',
'H4200': 'a girdle (mezach)',
'H4201': 'a girdle (meziach)',
'H4202': 'food (mazon)',
'H4203': 'food (mazon)',
'H4204': 'a wound (mazor)',
'H4205': 'a girdle (mazor)',
'H4206': 'a scattering (mezar)',
'H4207': 'a chamber (mezzev)',
'H4208': 'Mezahab (Mezahab)',
'H4209': 'a doorpost (mezuzah)',
'H4210': 'a sifting (mezarim)',
'H4211': 'to drain (matsah)',
'H4212': 'unleavened bread (matstsah)',
'H4213': 'unleavened bread (matstsah)',
'H4214': 'a melting (matsah)',
'H4215': 'a fixed spot (matstsab)',
'H4216': 'a garrison (matstsab)',
'H4217': 'a station (matstsebah)',
'H4218': 'a station (mutstsab)',
'H4219': 'a planting (matstsa)',
'H4220': 'a planting (matstsaah)',
'H4221': 'a station (mutstsabah)',
'H4222': 'a quarrel (matstsah)',
'H4223': 'a strife (matstsuth)',
'H4224': 'a setting (matstsab)',
'H4225': 'deep (metsach)',
'H4226': 'a forehead (metsach)',
'H4227': 'a greave (mitscha)',
'H4228': 'to flow down (matsats)',
'H4229': 'a bed (mitstsa)',
'H4230': 'a little (mitsar)',
'H4231': 'a little (mitstar)',
'H4232': 'a hiding place (mitsad)',
'H4233': 'a fastness (metsad)',
'H4234': 'a fortress (metsad)',
'H4235': 'to look (tsaphah)',
'H4236': 'a covering (mitspah)',
'H4237': 'a net (metsudah)',
'H4238': 'a step (mitsad)',
'H4239': 'a step (mitsad)',
'H4240': 'Mitspeh (Mitspeh)',
'H4241': 'a watchtower (mitspah)',
'H4242': 'a covering (michseh)',
'H4243': 'a number (miksah)',
'H4244': 'a choice (michlah)',
'H4245': 'a completion (michlah)',
'H4246': 'perfection (michlal)',
'H4247': 'gorgeous (michlol)',
'H4248': 'a hidden thing (michman)',
'H4249': 'treasure (mikmannim)',
'H4250': 'a net (mikmar)',
'H4251': 'a net (mikmoreth)',
'H4252': 'a treasure (misken)',
'H4253': 'storehouses (miskenoth)',
'H4254': 'a deed (mikneh)',
'H4255': 'a purchase (mikneh)',
'H4256': 'a pit (maktesh)',
'H4257': 'a writing (miktab)',
'H4258': 'gold (kethem)',
'H4259': 'a covering (miklal)',
'H4260': 'a garment (miktsoah)',
'H4261': 'an angle (maqtsua)',
'H4262': 'a corner (miktsoah)',
'H4263': 'a plane (maqtsoah)',
'H4264': 'a fortress (matsor)',
'H4265': 'a fortress (matsor)',
'H4266': 'a fortress (metsorah)',
'H4267': 'a defense (matsor)',
'H4268': 'a pounding (mechittah)',
'H4269': 'a terror (mechittah)',
'H4270': 'ruin (mechittah)',
'H4271': 'a chisel (machatsebah)',
'H4272': 'a dividing (mechqarah)',
'H4273': 'half (machtsith)',
'H4274': 'a division (mechitsah)',
'H4275': 'to grasp (macha)',
'H4276': 'Machi (Maki)',
'H4277': 'a pounding (maka)',
'H4278': 'a blow (makka)',
'H4279': 'a wound (makkah)',
'H4280': 'a wound (machah)',
'H4281': 'a fastening (mechabbereth)',
'H4282': 'a joining (mechubereth)',
'H4283': 'a blot (macheh)',
'H4284': 'a pan (machabath)',
'H4285': 'a covering (machseh)',
'H4286': 'a covering (machsom)',
'H4287': 'a bruising (matsor)',
'H4288': 'a thought (machashabah)',
'H4289': 'a thought (machashebeth)',
'H4290': 'darkness (machshak)',
'H4291': 'darkness (machsok)',
'H4292': 'to wipe (machah)',
'H4293': 'to wipe out (macha)',
'H4294': 'marrow (machah)',
'H4295': 'a window (mechazoth)',
'H4296': 'a vision (machazeh)',
'H4297': 'a port (machoz)',
'H4298': 'a cord (methar)',
'H4299': 'to fasten (mathach)',
'H4300': 'yesterday (timol)',
'H4301': 'yesterday (ethmol)',
'H4302': 'Methusael (Methushael)',
'H4303': 'Methuselah (Methushelach)',
'H4304': 'to sweeten (mathaq)',
'H4305': 'sweetness (metheq)',
'H4306': 'sweetness (mothaq)',
'H4307': 'sweetness (methaq)',
'H4308': 'a bridle (metheg)',
'H4309': 'Metheg-ammah (Metheg ha-Ammah)',
'H4310': 'to flow (nathak)',
'H4311': 'scabs (netheq)',
'H4312': 'Mithkah (Mithqah)',
'H4313': 'a gift (mattan)',
'H4314': 'a gift (mattana)',
'H4315': 'a gift (mattath)',
'H4316': 'a gift (mattath)',
'H4317': 'when (mathay)',
'H4318': 'Mithnite (Mithni)',
'H4319': 'Mithredath (Mithredath)',
'H4320': 'to die (muth)',
'H4321': 'death (maveth)',
'H4322': 'a place of death (maveth)',
'H4323': 'a fountain (mabbua)',
'H4324': 'confusion (mebukah)',
'H4325': 'water (mayim)',
'H4326': 'a swelling (mibbne)',
'H4327': 'a building (mibneh)',
'H4328': 'Mibsam (Mibsam)',
'H4329': 'Mibtsar (Mibtsar)',
'H4330': 'a fortress (mibtsar)',
'H4331': 'a fortress (mibtsarah)',
'H4332': 'Mebunnai (Mebunnay)',
'H4333': 'a boiling (mebashshelah)',
'H4334': 'a choice (mibchar)',
'H4335': 'a choice (mibchor)',
'H4336': 'a choice (mibchar)',
'H4337': 'a confidence (mibtach)',
'H4338': 'a confidence (mibtach)',
'H4339': 'a confidence (mibtachah)',
'H4340': 'to grow ripe (bagar)',
'H4341': 'to hasten (bahal)',
'H4342': 'alarm (behalah)',
'H4343': 'to marry (baal)',
'H4344': 'to reject (baal)',
'H4345': 'lord (beel)',
'H4346': 'a blot (moom)',
'H4347': 'a spot (mum)',
'H4348': 'to circumcise (mul)',
'H4349': 'a birth (moledeth)',
'H4350': 'progeny (moledeth)',
'H4351': 'to beget (yalad)',
'H4352': 'a birth (moledeth)',
'H4353': 'to circumcise (mul)',
'H4354': 'to advise (yaats)',
'H4355': 'to press (muq)',
'H4356': 'a mockery (moq)',
'H4357': 'to melt (mug)',
'H4358': 'to melt (mug)',
'H4359': 'a snare (moqesh)',
'H4360': 'a burning (moqed)',
'H4361': 'a hearth (moqedah)',
'H4362': 'to be poor (muk)',
'H4363': 'a foundation (mosad)',
'H4364': 'a foundation (mosad)',
'H4365': 'a foundation (mosadah)',
'H4366': 'a bond (moser)',
'H4367': 'a bond (moserah)',
'H4368': 'a band (moser)',
'H4369': 'a descent (morad)',
'H4370': 'a net (mikmar)',
'H4371': 'a net (mikmereth)',
'H4372': 'a net (mikmor)',
'H4373': 'a possession (miknah)',
'H4374': 'a purchase (miqneh)',
'H4375': 'to acquire (qanah)',
'H4376': 'a possession (miqneh)',
'H4377': 'a gathering (miqveh)',
'H4378': 'a gathering (miqveh)',
'H4379': 'a hope (miqveh)',
'H4380': 'a hope (miqvaah)',
'H4381': 'a shelter (michseh)',
'H4382': 'a number (miksah)',
'H4383': 'a writing (miktab)',
'H4384': 'a mortar (maktesh)',
'H4385': 'a mortar (maktesheth)',
'H4386': 'a place (makon)',
'H4387': 'a base (mekonah)',
'H4388': 'a base (mekunah)',
'H4389': 'a place (makom)',
'H4390': 'to be full (male)',
'H4391': 'to be full (male)',
'H4392': 'full (male)',
'H4393': 'fullness (melo)',
'H4394': 'fullness (melo)',
'H4395': 'a setting (milleah)',
'H4396': 'consecration (millu)',
'H4397': 'an angelic messenger (malak)',
'H4398': 'a messenger (malak)',
'H4399': 'work, message (melakah)',
'H4400': 'a message (malakuth)',
'H4401': 'an ambassador (malak)',
'H4402': 'a queen (malkah)',
'H4403': 'to be smooth (malats)',
'H4404': 'to escape (malat)',
'H4405': 'a fugitive (palit)',
'H4406': 'escape (peletah)',
'H4407': 'cement (melet)',
'H4408': 'a garment (malbush)',
'H4409': 'a garment (malbush)',
'H4410': 'a brick mold (malben)',
'H4411': 'Millo (Millo)',
'H4412': 'a rampart (meleah)',
'H4413': 'a rampart (meleah)',
'H4414': 'to rub (malach)',
'H4415': 'salt (melach)',
'H4416': 'salt (melach)',
'H4417': 'salt (melach)',
'H4418': 'saltiness (melechah)',
'H4419': 'a rag (melach)',
'H4420': 'a sailor (mallach)',
'H4421': 'to fight (lacham)',
'H4422': 'war (milchamah)',
'H4423': 'to be fat (malach)',
'H4424': 'to reign (malak)',
'H4425': 'to reign (melek)',
'H4426': 'a king (melek)',
'H4427': 'a king (melek)',
'H4428': 'a king (melek)',
'H4429': 'a queen (malka)',
'H4430': 'a kingdom (malku)',
'H4431': 'a kingdom (malku)',
'H4432': 'Molech (Molek)',
'H4433': 'Molecheth (Moleketh)',
'H4434': 'counsel (milkah)',
'H4435': 'a snare (milkudeth)',
'H4436': 'a kingdom (melukah)',
'H4437': 'a kingdom (malkuth)',
'H4438': 'a kingdom (malkuth)',
'H4439': 'Malluch (Malluk)',
'H4440': 'Malluchi (Malluki)',
'H4441': 'to advise (malak)',
'H4442': 'to advise (melek)',
'H4443': 'to nip (malaq)',
'H4444': 'a robe (maltaah)',
'H4445': 'wardrobe (meltachah)',
'H4446': 'a tooth (malthaa)',
'H4447': 'a steward (meltar)',
'H4448': 'to rule (mamal)',
'H4449': 'dominion (memel)',
'H4450': 'a kingdom (memlakah)',
'H4451': 'dominion (mamlakhah)',
'H4452': 'a kingdom (mamlakhuth)',
'H4453': 'a saying (mamlal)',
'H4454': 'a mixture (mimsek)',
'H4455': 'a mixture (mimsak)',
'H4456': 'a sale (mimkar)',
'H4457': 'a possession (mimkereth)',
'H4458': 'a rule (memshal)',
'H4459': 'dominion (memshalah)',
'H4460': 'dominion (memshalah)',
'H4461': 'Mamre (Mamre)',
'H4462': 'a bastard (mamzer)',
'H4463': 'a sprout (memer)',
'H4464': 'bitter (memerorim)',
'H4465': 'bitterness (memer)',
'H4466': 'bitterness (memeror)',
'H4467': 'a beating (mammath)',
'H4468': 'a death (mamoth)',
'H4469': 'a sweet drink (mimtach)',
'H4470': 'sweetness (mamtaqqim)',
'H4471': 'from (min)',
'H4472': 'from (min)',
'H4473': 'from (min)',
'H4474': 'a number (minyan)',
'H4475': 'to number (menah)',
'H4476': 'a number (mene)',
'H4477': 'Manoah (Manoach)',
'H4478': 'rest (manoach)',
'H4479': 'rest (menuchah)',
'H4480': 'to rain (matar)',
'H4481': 'rain (matar)',
'H4482': 'a prison (mattara)',
'H4483': 'a prison (mattara)',
'H4484': 'a gift (minchah)',
'H4485': 'a tribute (middah)',
'H4486': 'a tribute (mindah)',
'H4487': 'to know (yada)',
'H4488': 'knowledge (madda)',
'H4489': 'Manna (man)',
'H4490': 'a portion (manah)',
'H4491': 'Manasseh (Menashsheh)',
'H4492': 'Manassite (Menashshi)',
'H4493': 'forgetting (menashsheh)',
'H4494': 'a flight (manos)',
'H4495': 'a flight (menusah)',
'H4496': 'a lock (minel)',
'H4497': 'a lamp (menorah)',
'H4498': 'a weavers beam (manor)',
'H4499': 'a flight (manos)',
'H4500': 'to depart (manosh)',
'H4501': 'a water course (minharah)',
'H4502': 'Minni',
'H4503': 'Minnith',
'H4504': 'to assign, reckon (manah)',
'H4505': 'a portion (menah)',
'H4506': 'part (menah)',
'H4507': 'Manoach',
'H4508': 'from (minni)',
'H4509': 'Minyamin',
'H4510': 'a number (minyan)',
'H4511': 'to withhold, keep back (mana)',
'H4512': 'a withholding (mena)',
'H4513': 'a bolt, bar (manul)',
'H4514': 'from (minne)',
'H4515': 'to constitute (menah)',
'H4516': 'a measured portion (manah)',
'H4517': 'a part (manah)',
'H4518': 'a weight (maneh)',
'H4519': 'Menahem',
'H4520': 'a rest (menuchah)',
'H4521': 'rest (menuchah)',
'H4522': 'a resting place (manoach)',
'H4523': 'a resting place (manoach)',
'H4524': 'a flight (manos)',
'H4525': 'a place of refuge (manos)',
'H4526': 'a candlestick (menorah)',
'H4527': 'a weavers beam (manor)',
'H4528': 'refuge (menusah)',
'H4529': 'a cord (menni)',
'H4530': 'Mesha',
'H4531': 'a load, burden (massa)',
'H4532': 'threshing (masu)',
'H4533': 'a lifting up (massaah)',
'H4534': 'a burden (massah)',
'H4535': 'a pulling up (massa)',
'H4536': 'a quarry (massa)',
'H4537': 'a burden (maseth)',
'H4538': 'Masa',
'H4539': 'a prophecy (massa)',
'H4540': 'a melting (mas)',
'H4541': 'a tribute, levy (mas)',
'H4542': 'a melting (mes)',
'H4543': 'to gaze (masah)',
'H4544': 'a tribute (missah)',
'H4545': 'a covering (masveh)',
'H4546': 'a covering (masveh)',
'H4547': 'a covering (masak)',
'H4548': 'a covering (masak)',
'H4549': 'a covering (masseketh)',
'H4550': 'a cleaving (massaq)',
'H4551': 'sawed (massor)',
'H4552': 'a saw (massor)',
'H4553': 'a bond (misgereth)',
'H4554': 'to pine away, rot (masas)',
'H4555': 'to flow (masas)',
'H4556': 'a melting (masas)',
'H4557': 'a hiding place (mistor)',
'H4558': 'a hiding (mesethar)',
'H4559': 'to hire (masak)',
'H4560': 'Masrekah',
'H4561': 'a hiding place (mistar)',
'H4562': 'Me-zahab',
'H4563': 'a test, trial (massah)',
'H4564': 'a testing (massah)',
'H4565': 'a pouring (massekah)',
'H4566': 'a molten image (massekah)',
'H4567': 'poverty (miskenuth)',
'H4568': 'a gate (misderon)',
'H4569': 'a storehouse (miskenah)',
'H4570': 'poor (misken)',
'H4571': 'to number (mispar)',
'H4572': 'a spreading place (mishtoach)',
'H4573': 'desolation (meshamah)',
'H4574': 'to mix, mingle (masak)',
'H4575': 'mixed wine (mesek)',
'H4576': 'a mixture (mesek)',
'H4577': 'a cover (masak)',
'H4578': 'a gate (masger)',
'H4579': 'a smith (masger)',
'H4580': 'an enclosure (misgereth)',
'H4581': 'a border (misgereth)',
'H4D': 'H4582: a dwelling (maon)',
'H4583': 'a habitation (maon)',
'H4584': 'Maon',
'H4585': 'Meonothai',
'H4586': 'Meunim',
'H4587': 'an answer (maaneh)',
'H4588': 'a furrow (maanith)',
'H4589': 'a furrow (maanah)',
'H4590': 'a purpose (maan)',
'H4591': 'Meonothai',
'H4592': 'few, a little (meat)',
'H4593': 'a wrapping (maateh)',
'H4594': 'a mantle (maataphah)',
'H4595': 'a clod (maataphel)',
'H4596': 'Maai',
'H4597': 'the bowels (meah)',
'H4598': 'the stomach (meah)',
'H4599': 'Meath',
'H4600': 'a hundred (meah)',
'H4601': 'a hundredth (meah)',
'H4602': 'a heap (mai)',
'H4603': 'to rebel (maal)',
'H4604': 'an unfaithful act (maal)',
'H4605': 'unfaithfulness (maal)',
'H4606': 'Maai',
'H4607': 'above (maal)',
'H4608': 'an act of treachery (maal)',
'H4609': 'above (maal)',
'H4610': 'upward (maalah)',
'H4611': 'a step, stair (maalah)',
'H4612': 'a going up (maaleh)',
'H4613': 'an ascent (maaleh)',
'H4614': 'excellence (maalah)',
'H4615': 'a lift (maalah)',
'H4616': 'an advantage (maalah)',
'H4617': 'a deed (maalah)',
'H4618': 'a work (maaseh)',
'H4619': 'a work (maaseh)',
'H4620': 'a work (maaseh)',
'H4621': 'a work (maaseh)',
'H4622': 'a work (maaseh)',
'H4623': 'a work (maaseh)',
'H4624': 'a work (maaseh)',
'H4625': 'a work (maaseh)',
'H4626': 'a work (maaseh)',
'H4627': 'a work (maaseh)',
'H4628': 'a work (maaseh)',
'H4629': 'a work (maaseh)',
'H4630': 'a work (maaseh)',
'H4631': 'a work (maaseh)',
'H4632': 'a work (maaseh)',
'H4633': 'a work (maaseh)',
'H4634': 'a work (maaseh)',
'H4635': 'a work (maaseh)',
'H4636': 'a work (maaseh)',
'H4637': 'a work (maaseh)',
'H4638': 'a work (maaseh)',
'H4639': 'a work (maaseh)',
'H4640': 'a work (maaseah)',
'H4641': 'Maaseiah',
'H4642': 'Maasiai',
'H4643': 'a tithe (maaser)',
'H4644': 'a tithing (maaser)',
'H4645': 'Maath',
'H4646': 'Miphkad',
'H4647': 'a muster (miphkad)',
'H4648': 'an appointed place (miphkad)',
'H4649': 'a pressure (mippalah)',
'H4650': 'a ruin (mippalah)',
'H4651': 'a flake (mippal)',
'H4652': 'a falling (mippal)',
'H4653': 'a falling (mippalah)',
'H4File': 'H4654: a ruin (mappalah)',
'H4655': 'a choice part (mippalah)',
'H4656': 'a downfall (mappalah)',
'H4657': 'a refuse (mappal)',
'H4658': 'an escape (miphlat)',
'H4659': 'a wondrous work (miphlaah)',
'H4660': 'a wonder (miphlaah)',
'H4661': 'to crush (mapats)',
'H4662': 'a war club (mappets)',
'H4663': 'a shattering (mappats)',
'H4664': 'a shattering (mappats)',
'H4665': 'Miphkad',
'H4666': 'a breath (mappach)',
'H4667': 'a bellows (mappuach)',
'H4668': 'an object of dread (mappach)',
'H4669': 'an outlet (miphla)',
'H4670': 'a stream (miphla)',
'H4671': 'a stream (miphla)',
'H4672': 'to break forth (matsa)',
'H4Write': 'H4673: a finding (matsa)',
'H4674': 'to drain (matsah)',
'H4675': 'strife (matstsah)',
'H4676': 'unleavened bread (matstsah)',
'H4677': 'a garrison (matstsab)',
'H4678': 'a station (matstsab)',
'H4679': 'a standing place (matsab)',
'H4680': 'a garrison (matstsabah)',
'H4681': 'a pillar (matstsebah)',
'H4682': 'a pillar (matstsebah)',
'H4683': 'a pillar (matstsebah)',
'H4684': 'a pillar (matstsebah)',
'H4685': 'to place, set (matsag)',
'H4686': 'a setting (matsag)',
'H4687': 'a net (matsod)',
'H4688': 'a net (matsod)',
'H4689': 'a net (matsudah)',
'H4690': 'a fastness (matsud)',
'H4691': 'a fastness (matsud)',
'H4692': 'a fastness (matsudah)',
'H4693': 'a siege (matsor)',
'H4694': 'a siege (matsor)',
'H4695': 'a bulwark (matsor)',
'H4696': 'Mizraim',
'H4697': 'distress (matsor)',
'H4698': 'distress (metsurah)',
'H4699': 'distress (metsurah)',
'H4700': 'to suck (matsats)',
'H4701': 'a sucking (matsats)',
'H4702': 'a bed (matsa)',
'H4703': 'a couch (matsa)',
'H4704': 'Mizpah',
'H4705': 'a setting (mitspah)',
'H4706': 'a watchtower (mitspah)',
'H4707': 'Mizpeh',
'H4708': 'a watchtower (mitspah)',
'H4709': 'a watchtower (mitspah)',
'H4710': 'a watchtower (mitspah)',
'H4711': 'a watchtower (mitspah)',
'H4712': 'a watchtower (mitspah)',
'H4713': 'a spreading (mitsad)',
'H4714': 'Mizraim',
'H4715': 'a little (mitsar)',
'H4716': 'a little (mitsar)',
'H4717': 'a step (mitsad)',
'H4718': 'a marching (mitsad)',
'H4719': 'a turban (mitsnepheth)',
'H4720': 'a small thing (mitar)',
'H4721': 'a small thing (mitar)',
'H4722': 'a small thing (mitar)',
'H4723': 'a place (maqom)',
'H4724': 'a place (maqom)',
'H4725': 'a place (maqom)',
'H4726': 'a place (maqom)',
'H4727': 'a place (maqom)',
'H4728': 'a place (maqom)',
'H4729': 'a place (maqom)',
'H4730': 'a place (maqom)',
'H4731': 'a place (maqom)',
'H4732': 'a place (maqom)',
'H4733': 'to take, get (maqach)',
'H4734': 'a taking (miqqach)',
'H4735': 'a receiving (miqqach)',
'H4736': 'an article (miqnah)',
'H4737': 'a possession (miqnah)',
'H4738': 'a possession (miqnah)',
'H4739': 'a possession (miqnah)',
'H4740': 'a possession (miqneh)',
'H4741': 'a fold (miqneh)',
'H4742': 'a place of assembly (miqra)',
'H4743': 'a convocation (miqra)',
'H4744': 'a reading (miqra)',
'H4745': 'an occurrence (miqreh)',
'H4746': 'a chance (miqreh)',
'H4747': 'a building (miqrah)',
'H4748': 'a cooling (miqrah)',
'H4749': 'a cooling (miqreh)',
'H4SO': 'H4750: a refuge (miqlat)',
'H4751': 'a carving (miqlaath)',
'H4752': 'a sling (miqlaath)',
'H4753': 'a work of a turner (miqlaath)',
'H4754': 'to mock (maq)',
'H4755': 'to be bitter (mar)',
'H4756': 'Mara',
'H4757': 'to rebel (marad)',
'H4758': 'a mirror (mara)',
'H4759': 'sight, vision (maraah)',
'H4760': 'a vision (maraah)',
'H4761': 'a vision (maraah)',
'H4762': 'a vision (maraah)',
'H4763': 'a vision (maraah)',
'H4764': 'a vision (maraah)',
'H4765': 'a vision (maraah)',
'H4766': 'a vision (maraah)',
'H4767': 'a vision (maraah)',
'H4768': 'a vision (maraah)',
'H4769': 'a vision (maraah)',
'H4770': 'a vision (maraah)',
'H4771': 'Maralah',
'H4772': 'a vision (marah)',
'H4773': 'a vision (marah)',
'H4774': 'a vision (marah)',
'H4775': 'rebellion (mered)',
'H4776': 'rebellion (mered)',
'H4777': 'rebellion (mered)',
'H4778': 'rebellion (mered)',
'H4779': 'rebellious (mered)',
'H4780': 'rebellious (mered)',
'H4781': 'rebellion (merud)',
'H4782': 'a vision (marah)',
'H4783': 'Mered',
'H4784': 'to be rebellious (marah)',
'H4785': 'bitter (marah)',
'H4786': 'bitterness (morah)',
'H4787': 'bitterness (morah)',
'H4788': 'a rash (marach)',
'H4789': 'Meraioth',
'H4790': 'Meraioth',
'H4791': 'Meraioth',
'H4792': 'Meraiah',
'H4793': 'fat (meri)',
'H4794': 'fatling (meri)',
'H4795': 'Meribah',
'H4796': 'contention (meribah)',
'H4797': 'contention (meribah)',
'H4798': 'Merib-baal',
'H4799': 'Merib-baal',
'H4800': 'fatling (meri)',
'H4801': 'fatling (meri)',
'H4802': 'fatling (meri)',
'H4803': 'fatling (meri)',
'H4804': 'fatling (meri)',
'H4805': 'rebellion (meri)',
'H4806': 'bitter (marir)',
'H4807': 'bitter (marir)',
'H4808': 'bitter (mariri)',
'H4809': 'Merarite',
'H4810': 'Merari',
'H4811': 'a chariot (merkab)',
'H4812': 'a seat (merkab)',
'H4813': 'a chariot (merkabah)',
'H4814': 'a chariot (merkabah)',
'H4815': 'a chariot (merkabah)',
'H4816': 'a chariot (merkabah)',
'H4817': 'a chariot (merkabah)',
'H4818': 'a riding (merkab)',
'H4819': 'a rest (margia)',
'H4820': 'to stone (ragam)',
'H4821': 'a heap (rigmah)',
'H4822': 'a heap (rigmah)',
'H4823': 'a friend (markoleth)',
'H4Try': 'H4824: a heap (margemah)',
'H4825': 'a quiet (margoa)',
'H4826': 'a place of rest (margeah)',
'H4827': 'a place of rest (margeah)',
'H4828': 'to carve (marad)',
'H4829': 'a spreading (marbad)',
'H4830': 'a covering (marbad)',
'H4831': 'to multiply (rabah)',
'H4832': 'a stall (marbeq)',
'H4833': 'a treading (mirmas)',
'H4834': 'a trampling (mirmas)',
'H4835': 'to be bitter (marar)',
'H4836': 'a drop (mar)',
'H4837': 'a drop (mar)',
'H4838': 'bitter (mar)',
'H4839': 'bitter (mar)',
'H4840': 'bitter (mar)',
'H4841': 'bitter (mar)',
'H4842': 'bitter (mar)',
'H4843': 'bitter (mar)',
'H4844': 'bitterness (meror)',
'H4845': 'bitterness (meror)',
'H4846': 'bitterness (merorah)',
'H4847': 'a bitter thing (merorah)',
'H4848': 'bitterness (merirah)',
'H4849': 'bitterness (meriri)',
'H4850': 'bitterness (meriri)',
'H4851': 'a bitter thing (merorah)',
'H4852': 'a bitter thing (merorah)',
'H4853': 'to rebel (marad)',
'H4854': 'rebellion (merad)',
'H4855': 'Mordecai',
'H4856': 'Merodach',
'H4857': 'Merodach-baladan',
'H4858': 'a healing (marpe)',
'H4859': 'a healing (marpe)',
'H4860': 'a healing (marpe)',
'H4861': 'a healing (marpe)',
'H4862': 'cessation, annihilation (mishbath)',
'H4863': 'checkered work (mishbetsah)',
'H4864': 'a gathering (masgereth)',
'H4865': 'a flowing (mabbol)',
'H4866': 'a flowing (mabbol)',
'H4867': 'a flowing (mabbol)',
'H4868': 'a flowing (mabbol)',
'H4869': 'a snare (mishbar)',
'H4870': 'a breaking (mishbar)',
'H4871': 'a snare (mishbar)',
'H4872': 'Meshobab',
'H4873': 'a turning away (meshubah)',
'H4874': 'a turning away (meshubah)',
'H4875': 'a turning away (meshubah)',
'H4876': 'a turning away (meshubah)',
'H4877': 'a turning away (meshubah)',
'H4878': 'a turning away (meshubah)',
'H4879': 'a turning away (meshubah)',
'H4880': 'a turning away (meshubah)',
'H4881': 'a turning away (meshubah)',
'H4882': 'a saw (massor)',
'H4883': 'a saw (massor)',
'H4884': 'a rule (misrah)',
'H4885': 'a rule (misrah)',
'H4886': 'to anoint (mashach)',
'H4887': 'to anoint (meshach)',
'H4888': 'anointed (mishchah)',
'H4889': 'anointed (mishchah)',
'H4890': 'anointed (mishchah)',
'H4891': 'anointed (mishchah)',
'H4892': 'anointed (mishchah)',
'H4893': 'anointed (mishchah)',
'H4894': 'anointed (mishchah)',
'H4895': 'anointed (mishchah)',
'H4896': 'anointed (mishchah)',
'H4897': 'anointed (mishchah)',
'H4898': 'anointed (mishchah)',
'H4899': 'anointed one (mashiach)',
'H4900': 'to draw (mashak)',
'H4901': 'a drawing (meshek)',
'H4902': 'a possession (meshek)',
'H4903': 'a possession (meshek)',
'H4904': 'a rope (moshekah)',
'H4905': 'a trail (mishkan)',
'H4SO': 'H4906: a dwelling (mishkan)',
'H4907': 'a dwelling (mishkan)',
'H4908': 'a dwelling (mishkan)',
'H4909': 'a dwelling (mishkan)',
'H4910': 'to rule (mashal)',
'H4911': 'to rule (meshal)',
'H4912': 'a proverb (mashal)',
'H4913': 'a proverb (mashal)',
'H4914': 'a proverb (mashal)',
'H4915': 'a proverb (mashal)',
'H4916': 'a proverb (mashal)',
'H4917': 'a proverb (mashal)',
'H4918': 'a proverb (mashal)',
'H4919': 'a proverb (mashal)',
'H4920': 'a proverb (mashal)',
'H4921': 'a proverb (mashal)',
'H4922': 'a proverb (mashal)',
'H4923': 'a proverb (mashal)',
'H4924': 'a proverb (mashal)',
'H4925': 'a proverb (mashal)',
'H4926': 'a proverb (mashal)',
'H4927': 'a proverb (mashal)',
'H4928': 'a proverb (mashal)',
'H4929': 'a proverb (mashal)',
'H4930': 'a proverb (mashal)',
'H4931': 'a proverb (mashal)',
'H4932': 'a proverb (mashal)',
'H4933': 'a proverb (mashal)',
'H4934': 'a proverb (mashal)',
'H4SO': 'H4935: a proverb (mashal)',
'H4936': 'a proverb (mashal)',
'H4937': 'a proverb (mashal)',
'H4938': 'a proverb (mashal)',
'H4939': 'a proverb (mashal)',
'H4940': 'a proverb (mashal)',
'H4941': 'weight (mishqol)',
'H4942': 'weight (mishqal)',
'H4943': 'a buttress (mishqeeth)',
'H4944': 'a running (mesheq)',
'H4945': 'a watering (mashqeh)',
'H4946': 'a drinking (mashqeh)',
'H4947': 'a drinking (mashqeh)',
'H4948': 'a lintel (mashqoph)',
'H4949': 'a weight (mishqeleth)',
'H4950': 'a settling place (of water) (mishqa)',
'H4951': 'dominion, rule (misrah)',
'H4952': 'juice (of grapes) (mishrah)',
'H4953': 'a (musical) pipe, flute (mashrowqiy)',
'H4954': 'a Mishraite (Mishraiy)',
'H4955': 'a burning (misraphah)',
'H4956': 'Misrephoth-maim, a place (Misrephowth Mayim)',
'H4957': 'Masrekah, a place (Masreqah)',
'H4958': 'a pan (masreth)',
'H4SO': 'H4959: to feel, grope (mashash)',
'H4960': 'a feast, banquet (mishteh)',
'H4961': 'a banquet (Aramaic) (mishteh)',
'H4962': 'man, male, person (math)',
'H4963': 'a straw heap (mathben)',
'H4964': 'a bit, bridle (metheg)',
'H4965': 'Metheg-ha-ammah, a place (Metheg ha-Ammah)',
'H4966': 'sweet, sweetness (mathowq)',
'H4967': 'Methusael (Methuwshael)',
'H4968': 'Methuselah (Methuwshelach)',
'H4969': 'to stretch out, spread (mathach)',
'H4970': 'when? how long? (mathay)',
'H4971': 'measurement, proportion, tale (mathkoneth)',
'H4972': 'weariness, hardship (mattelaah)',
'H4973': 'a biter, a tooth, jaw (methallaah)',
'H4974': 'soundness, entirety (methom)',
'H4975': 'loins, hips (mothen)',
'H4976': 'a present, gift (mattan)',
'H4977': 'Mattan (Mattan)',
'H4978': 'a gift (Aramaic) (mattana)',
'H4979': 'a present, gift (mattanah)',
'H4980': 'Mattanah, a place (Mattanah)',
'H4981': 'a Mithnite (Mithniy)',
'H4982': 'Mattenai, three Israelites (Mattenay)',
'H4983': 'Mattanyah (Mattanyah)',
'H4984': 'supreme exaltation (mithnasse)',
'H4985': 'to be or become sweet (mathaq)',
'H4986': 'sweetness (metheq)',
'H4987': 'sweetness (motheq)',
'H4988': 'to feed sweetly, be sweet (mathaq)',
'H4989': 'Mithcah, a place (Mithqah)',
'H4990': 'Mithredath, a Persian name (Mithredath)',
'H4991': 'a gift, reward (mattath)',
'H4992': 'Mattattah, an Israelite (Mattattah)',
'H4993': 'Mattithiah (Mattithyah)',
'H4994': 'I pray, now, please (na)',
'H4995': 'raw, uncooked (na)',
'H4996': 'No (Thebes), a city in Egypt (No)',
'H4997': 'a (skin or leather) bag, bottle (nod)',
'H4998': 'to be comely, be beautiful (naah)',
'H4999': 'a home, pasture, habitation (naah)',
'H5000': 'suitable, comely, beautiful (naveh)',
















































































    # G (Greek) 1..1128
    "G1": "the first; alpha", "G2": "a, an (indefinite article)", "G3": "affirmation (particle)", "G4": "to lead, bring", "G5": "to bind",
    "G6": "to loose", "G7": "to call, name", "G8": "to do, make", "G9": "to be", "G10": "to have, hold",
    "G11": "to see, look", "G12": "to speak, say", "G13": "to send", "G14": "to come", "G15": "to go",
    "G16": "to love (verb)", "G17": "to live, dwell", "G18": "to die", "G19": "to raise up", "G20": "to teach",
    "G21": "to hear", "G22": "to give", "G23": "to reveal", "G24": "to judge", "G25": "to begin",
    "G26": "christos — anointed (christ)", "G27": "kyrios — lord", "G28": "theos — god", "G29": "iesous — jesus", "G30": "pneuma — spirit, wind",
    "G31": "logos — word, reason", "G32": "agape — love (noun)", "G33": "phileo — love (verb)", "G34": "dikaios — righteous", "G35": "dikaiosune — righteousness",
    "G36": "ekklesia — assembly, church", "G37": "baptizo — to immerse", "G38": "euangelion — good news", "G39": "martyria — testimony", "G40": "soteria — salvation",
    "G41": "soter — savior", "G42": "metanoia — repentance", "G43": "eirene — peace", "G44": "pistis — faith", "G45": "ethnos — nation",
    "G46": "kosmos — world", "G47": "charis — grace", "G48": "charisma — gift", "G49": "episkope — oversight", "G50": "diakonos — servant, minister",
    "G51": "apostolos — apostle", "G52": "propheteia — prophecy", "G53": "therapeia — healing", "G54": "logos (word)", "G55": "soma — body",
    "G56": "psuche — soul", "G57": "zoe — life", "G58": "thanatos — death", "G59": "pharmakon — medicine, potion", "G60": "krisis — judgment",
    "G61": "hypocrisis — pretense", "G62": "anastasis — resurrection", "G63": "erchomai — to come", "G64": "metamelomai — to regret", "G65": "gnosis — knowledge",
    "G66": "epignosis — full knowledge", "G67": "sophia — wisdom", "G68": "doxa — glory", "G69": "telos — end, goal", "G70": "zosimos — lively (rare)",
    "G71": "koinonia — fellowship", "G72": "hypostasis — substance, reality", "G73": "theourgos — worker for god", "G74": "ekeinos — that one", "G75": "autos — self",
    "G76": "allos — other", "G77": "adapanos — without cost, gratis", "G78": "parakletos — advocate, comforter", "G79": "ekklesia — congregation (alt sense)", "G80": "diathesis — arrangement, covenant",
    "G81": "the feeling of brotherliness", "G82": "hidden", "G83": "uncertainty", "G84": "uncertainly", "G85": "to be in distress",
    "G86": "unseen", "G87": "undistinguished", "G88": "uninterrupted, i.e. permanent, unceasing", "G89": "uninterruptedly, unceasingly", "G90": "incorruptibleness",
    "G91": "to be unjust", "G92": "a wrong done", "G93": "injustice", "G94": "unjust", "G95": "unjustly",
    "G96": "unapproved, i.e. rejected", "G97": "without deceit, honest, sincere", "G98": "adramyttene or belonging to adramyttium", "G99": "the adriatic sea", "G100": "plumpness",
    "G101": "to be unable", "G102": "unable, i.e. weak", "G103": "to sing", "G104": "\"ever\"", "G105": "an eagle",
    "G106": "unleavened", "G107": "azor, an israelite", "G108": "azotus , a place in israel", "G109": "\"air\"", "G110": "deathlessness, immortality",
    "G111": "illegal", "G112": "without god", "G113": "lawless", "G114": "to set aside", "G115": "cancellation",
    "G116": "athens, the capitol of greece", "G117": "an athenian, an inhabitant of athens", "G118": "to contend in the competitive games", "G119": "a struggle", "G120": "to be spiritless, i.e. disheartened",
    "G121": "not guilty", "G122": "belonging to a goat", "G123": "a beach", "G124": "an egyptian or inhabitant of egypt", "G125": "egypt , the land of the nile",
    "G126": "eternal", "G127": "bashfulness", "G128": "an ethiopian", "G129": "blood", "G130": "an effusion of blood",
    "G131": "to flow blood, i.e. have a hemorrhage", "G132": "aeneas, an israelite", "G133": "a praising", "G134": "to praise", "G135": "an obscure saying, \"enigma\"",
    "G136": "a story", "G137": "ænon, a place in israel", "G138": "to take for oneself, i.e. to prefer", "G139": "a choice", "G140": "to make a choice",
    "G141": "schismatic, discordant, divisive", "G142": "to lift up", "G143": "to perceive", "G144": "perception", "G145": "an organ of perception",
    "G146": "characterized by sordid, disgraceful gain", "G147": "to gain in a disgracefully, sordidly manner", "G148": "vile, disgraceful conversation", "G149": "a shameful thing, i.e. of improper conduct", "G150": "shameful, disgraceful, i.e. base",
    "G151": "shamefulness, i.e. obscenity", "G152": "shame, disgrace", "G153": "to feel shame", "G154": "to ask", "G155": "a thing asked",
    "G156": "a cause", "G157": "a thing charged", "G158": "a reason or crime", "G159": "causative", "G160": "unexpected",
    "G161": "captivity", "G162": "to capture", "G163": "to make captive", "G164": "a prisoner of war", "G165": "an age",
    "G166": "perpetual", "G167": "impurity", "G168": "impurity", "G169": "impure", "G170": "to be unseasonable, out of season",
    "G171": "unseasonably", "G172": "not bad", "G173": "a thorn", "G174": "thorny", "G175": "barren",
    "G176": "unblamable", "G177": "unveiled", "G178": "without trial", "G179": "indissoluble", "G180": "unrefraining",
    "G181": "instability, i.e. disorder", "G182": "inconstant", "G183": "unrestrainable", "G184": "akeldama, a place near jerusalem", "G185": "unmixed",
    "G186": "not leaning", "G187": "to make a point", "G188": "just now, i.e. still", "G189": "hearing", "G190": "to be in the same way with, i.e. to accompany",
    "G191": "to hear", "G192": "want of self-restraint", "G193": "powerless, i.e. without self-control", "G194": "undiluted", "G195": "exactness",
    "G196": "most exact", "G197": "more exactly", "G198": "to be exact, i.e. ascertain", "G199": "exactly", "G200": "a locust",
    "G201": "an audience-room, i.e. courtroom", "G202": "a hearer", "G203": "the foreskin", "G204": "belonging to the extreme corner", "G205": "the top of the heap",
    "G206": "the extremity", "G207": "akulas, an israelite", "G208": "to invalidate", "G209": "in an unhindered manner, i.e. freely", "G210": "unwilling, involuntary",
    "G211": "an \"alabaster\" box", "G212": "empty boasting, mere bragging", "G213": "a boaster or braggart", "G214": "to cry out loudly , clamor", "G215": "unspeakable",
    "G216": "mute", "G217": "salt", "G218": "to rub with oil", "G219": "cock-crow", "G220": "a cock or male fowl",
    "G221": "an alexandreian or inhabitant of alexandria", "G222": "alexandrine, or belonging to alexandria", "G223": "man-defender", "G224": "flour", "G225": "truth",
    "G226": "to be true", "G227": "true", "G228": "truthful", "G229": "to grind", "G230": "truly",
    "G231": "a sailor", "G232": "to be a fisher", "G233": "to salt", "G234": "defilement", "G235": "other things",
    "G236": "to change, transform, make different", "G237": "from elsewhere", "G238": "to allegorize, make into a allegory", "G239": "praise ye jah!, an adoring exclamation", "G240": "one another",
    "G241": "foreign, i.e. not a jew", "G242": "to jump", "G243": "\"else,\" i.e. different", "G244": "overseeing others' affairs, i.e. a meddler", "G245": "another's, i.e. not one's own",
    "G246": "foreign", "G247": "differently", "G248": "to tread out grain", "G249": "irrational", "G250": "aloes",
    "G251": "\"salt\"", "G252": "briny", "G253": "more without grief", "G254": "a fetter or manacle", "G255": "unprofitable, gainless",
    "G256": "alphoeus, an israelite", "G257": "a threshing-floor", "G258": "a fox", "G259": "capture", "G260": "at the \"same\" time",
    "G261": "ignorant", "G262": "\"amaranthine\", a flower that never withers or...", "G263": "unfading", "G264": "to miss the mark (and so not share in the prize)", "G265": "a sin",
    "G266": "a sin", "G267": "unattested", "G268": "sinful, i.e. a sinner", "G269": "peaceable", "G270": "to collect",
    "G271": "the \"amethyst\"", "G272": "to be careless of", "G273": "irreproachable", "G274": "faultlessly", "G275": "not anxious",
    "G276": "unchangeable", "G277": "immovable", "G278": "irrevocable", "G279": "unrepentant", "G280": "immoderate",
    "G281": "firm", "G282": "motherless, i.e. of unknown maternity", "G283": "unsoiled", "G284": "aminadab, an israelite", "G285": "sand",
    "G286": "a lamb", "G287": "compensate", "G288": "a vine", "G289": "a vine-worker, i.e. pruner", "G290": "a vineyard",
    "G291": "amplias, a roman christian", "G292": "to ward off , i.e. protect", "G293": "a net (as thrown about the fish)", "G294": "to enrobe", "G295": "a city surrounded by a river",
    "G296": "a fork in the road", "G297": "both", "G298": "unblamable", "G299": "unblemished", "G300": "amon, an israelite",
    "G301": "amos, an israelite", "G302": "denoting a supposition, wish, possibility or un...", "G303": "up", "G304": "a stairway", "G305": "to go up",
    "G306": "to put off", "G307": "to cause to go up, i.e. haul", "G308": "to look up", "G309": "restoration of sight", "G310": "to raise a cry",
    "G311": "a putting off", "G312": "to announce", "G313": "to beget", "G314": "to know again", "G315": "to necessitate",
    "G316": "necessary", "G317": "compulsorily", "G318": "constraint", "G319": "to make known", "G320": "reading",
    "G321": "to lead up", "G322": "to exhibit", "G323": "exhibition", "G324": "to entertain", "G325": "to hand over",
    "G326": "to recover life", "G327": "to search out", "G328": "to gird afresh", "G329": "to re-enkindle", "G330": "to revive",
    "G331": "a ban", "G332": "to bind with a vow under penalty of curse and d...", "G333": "to look again at", "G334": "a offering in fulfillment of a vow", "G335": "impudence",
    "G336": "execution, the act of killing", "G337": "to take up", "G338": "innocent", "G339": "to set up", "G340": "to restore",
    "G341": "to renovate", "G342": "renovation", "G343": "to unveil", "G344": "to turn back", "G345": "to recline at a meal",
    "G346": "to sum up", "G347": "to lean back", "G348": "to beat back, i.e. check", "G349": "to scream out", "G350": "to scrutinize",
    "G351": "a investigation", "G352": "to unbend, i.e. rise", "G353": "to take up", "G354": "ascension", "G355": "to use up, i.e. destroy",
    "G356": "proportion", "G357": "to estimate", "G358": "unsalty, saltless", "G359": "departure", "G360": "to break up, i.e. depart",
    "G361": "sinless", "G362": "to patiently await", "G363": "to remind and admonish", "G364": "recollection", "G365": "to renew, renovate, i.e. reform",
    "G366": "to become sober again", "G367": "ananias, the name of three israelites", "G368": "indisputable, without dispute", "G369": "without disputing", "G370": "of dissimilar weight or value",
    "G371": "weighing or valuing differently", "G372": "intermission", "G373": "to repose, to rest", "G374": "to incite", "G375": "to send back",
    "G376": "crippled", "G377": "to fall back, i.e. lie down, lean back", "G378": "to very fully complete", "G379": "unjustifiable, indefensible, inexcusable", "G380": "to unroll",
    "G381": "to enkindle", "G382": "unnumbered, i.e. without number", "G383": "to shake up", "G384": "to pack up (baggage)", "G385": "to draw out",
    "G386": "a standing up again", "G387": "to drive out of home", "G388": "to recrucify", "G389": "to sigh deeply", "G390": "to overturn",
    "G391": "behavior", "G392": "to compose", "G393": "to arise", "G394": "to set forth , i.e propound, declare", "G395": "a rising of light",
    "G396": "to upturn", "G397": "to rear", "G398": "to show", "G399": "to bear up, carry up", "G400": "to speak out, exclaim",
    "G401": "effusion", "G402": "to depart", "G403": "a recovery of breath", "G404": "to cool off", "G405": "an enslaver",
    "G406": "manly", "G407": "to act manly", "G408": "man of victory", "G409": "a manslayer, i.e. a murderer", "G410": "unaccused",
    "G411": "not expounded in full, i.e. indescribable", "G412": "not spoken out", "G413": "not left out", "G414": "more endurable", "G415": "merciless",
    "G416": "to toss with the wind", "G417": "wind", "G418": "unadmitted", "G419": "not searched out", "G420": "enduring of ill, i.e. forbearing",
    "G421": "not tracked out", "G422": "not ashamed, i.e. irreprehensible", "G423": "not arrested", "G424": "to ascend", "G425": "relaxation",
    "G426": "to investigate", "G427": "without", "G428": "not well placed", "G429": "to find out", "G430": "to hold oneself up against",
    "G431": "akin", "G432": "dill", "G433": "to attain to", "G434": "savage", "G435": "a man, an individual male",
    "G436": "to stand against, i.e. oppose", "G437": "to confess in turn, i.e. respond in praise", "G438": "a blossom", "G439": "a bed of burning coals", "G440": "a live coal",
    "G441": "man-courting, i.e. fawning", "G442": "human, mankind", "G443": "a manslayer", "G444": "man-faced", "G445": "to act as proconsul",
    "G446": "instead of the highest officer", "G447": "to let up", "G448": "inexorable", "G449": "uncleansed", "G450": "to stand up",
    "G451": "anna, an israelitess", "G452": "annas, an israelite", "G453": "unintelligent", "G454": "stupidity", "G455": "to open up",
    "G456": "to rebuild", "G457": "opening", "G458": "illegality, i.e. violation of law", "G459": "lawless", "G460": "lawlessly",
    "G461": "to straighten up", "G462": "unholy, wicked", "G463": "self-restraint, i.e. tolerance", "G464": "to struggle against", "G465": "an equivalent or ransom",
    "G466": "to supplement", "G467": "to requite", "G468": "a requital", "G469": "requital", "G470": "to contradict or dispute",
    "G471": "to speak against", "G472": "to hold oneself opposite to", "G473": "opposite, i.e. instead or because", "G474": "to toss back and forth", "G475": "to set oneself opposite, i.e. be  disputatious",
    "G476": "an opponent or adversary", "G477": "opposition, i.e. a conflict", "G478": "to set down against, i.e. withstand", "G479": "to invite in return", "G480": "to lie opposite, i.e. be adverse to",
    "G481": "opposite", "G482": "to take hold of in turn, i.e. grasp, claim", "G483": "correspondent to reality", "G484": "to set out opposite, i.e. represent", "G485": "a representation or (specifically) resemblance",
    "G486": "to fall opposite to, i.e. meet with", "G487": "meeting with", "G488": "to set one's face against, i.e. resist", "G489": "a counterpart or copy", "G490": "a counterplot or contradiction",
    "G491": "to lay against, i.e. oppose", "G492": "to place alongside, i.e. present", "G493": "to draw opposite, i.e. confront", "G494": "to serve in place of", "G495": "a counterpart, i.e. duplicate",
    "G496": "to arrange against, i.e. marshal", "G497": "to wait contrary, i.e. in ambush", "G498": "to take hold of opposite, i.e. participate", "G499": "to lift oneself against, i.e. oppose", "G500": "without rebuke, unblamable",
    "G501": "antioch, a place in syria", "G502": "an antiocheian or inhabitant of antiochia", "G503": "antipater, an israelite", "G504": "antipatris, a place in palestine", "G505": "on the opposite bank",
    "G506": "to pass over", "G507": "to be instead of, i.e. be parallel", "G508": "unploughed", "G509": "to go by", "G510": "to measure off against",
    "G511": "a corresponding gift", "G512": "corresponding in rank", "G513": "a corresponding price, i.e. redemption", "G514": "irrigation, refreshing", "G515": "to cool off",
    "G516": "worthless", "G517": "topmost", "G518": "to disbelieve", "G519": "disbelief", "G520": "faithless, i.e. disbelieving",
    "G521": "disobedient, i.e. contumacious", "G522": "disobedience, i.e. contumacy", "G523": "from some time", "G524": "to take away entirely, i.e. abolish", "G525": "to take off wholly, i.e. make bare",
    "G526": "from", "G527": "to receive from", "G528": "to take fully, i.e. adopt", "G529": "a receipt", "G530": "apelles, a christian",
    "G531": "to get away from, i.e. escape or observe", "G532": "hope deferred", "G533": "to unroll, i.e. lay open", "G534": "to lead away, i.e. seduce", "G535": "a detachment",
    "G536": "to pay off", "G537": "to separate, i.e. determine", "G538": "to leave, i.e. permit", "G539": "thoroughly", "G540": "to give away, i.e. up, over, back, etc.",
    "G541": "boldness, freedom, openness", "G542": "to be frank, speak freely", "G543": "to lead away", "G544": "to drive off", "G545": "to go away, i.e. depart or disappear",
    "G546": "to look away from", "G547": "to wipe off", "G548": "to lay aside", "G549": "to get off", "G550": "to receive in full",
    "G551": "to know fully", "G552": "to put to death entirely", "G553": "to press fully, i.e. strangle", "G554": "to select out", "G555": "to wash away",
    "G556": "to lose away, i.e. become destitute", "G557": "to shed off", "G558": "to finish off, i.e. expire", "G559": "to die off", "G560": "to loose away",
    "G561": "to break off", "G562": "to destroy fully", "G563": "unprofitable", "G564": "to rinse off", "G565": "a departure, i.e. decease",
    "G566": "to be absent", "G567": "to sail away", "G568": "to try fully, i.e. scrutinize", "G569": "to disbelieve", "G570": "faithless, disbelieving",
    "G571": "disobedience, disbelief", "G572": "unpersuadable", "G573": "simple, innocent, candid", "G574": "innocence, sincerity, candor", "G575": "from",
    "G576": "to bring off", "G577": "to take off", "G578": "to be absent", "G579": "a seeing, i.e. the function of sight", "G580": "to set off by boundary, i.e. separate",
    "G581": "a designation", "G582": "a marking off, i.e. specification", "G583": "to cast off, i.e. reject", "G584": "to wander away", "G585": "to cause to revolt",
    "G586": "to depart", "G587": "to trip up", "G588": "a deposit, i.e. trust", "G589": "to flow off", "G590": "to pour forth",
    "G591": "to deliver", "G592": "to take off", "G593": "to breathe out, i.e. expire", "G594": "to set apart, i.e. exclude", "G595": "to move down from",
    "G596": "a falling off, i.e. apostasy", "G597": "divorce, repudiation", "G598": "to keep off or Sandusky", "G599": "to send away, i.e. release", "G600": "to mislead",
    "G601": "to defraud", "G602": "disclosure, revelation", "G603": "to take off the cover, i.e. reveal", "G604": "to watch keenly", "G605": "a watching from afar, i.e. expectation",
    "G606": "to decapitate", "G607": "to hide away", "G608": "to hide from", "G609": "to cause to go forth", "G610": "to reproduce",
    "G611": "to lie away, i.e. be reserved", "G612": "to die away", "G613": "to judge of, i.e. determine", "G614": "a decision", "G615": "to answer",
    "G616": "a reply", "G617": "to roll away", "G618": "to receive", "G619": "full enjoyment", "G620": "a taking away",
    "G621": "to enjoy fully", "G622": "to destroy fully", "G623": "destroying angel", "G624": "apollonia, a place in macedonia", "G625": "apollo",
    "G626": "to make excuse", "G627": "an apology or defense", "G628": "to load off", "G629": "to free from", "G630": "to wash off",
    "G631": "to cleanse away", "G632": "to assign to", "G633": "to travel", "G634": "a denizen", "G635": "to be at a loss",
    "G636": "to lose oneself", "G637": "to shed down", "G638": "to press heavily upon", "G639": "to send forth", "G640": "apostolic",
    "G641": "a sending away, i.e. dismissal", "G642": "to render unsavory", "G643": "completeness", "G644": "to shade down, i.e. darken", "G645": "to shake off",
    "G646": "a delegate", "G647": "commission", "G648": "to apostatize", "G649": "to send away", "G650": "to hate utterly",
    "G651": "to store away", "G652": "a repository", "G653": "to turn away or back", "G654": "abrupt", "G655": "sharply",
    "G656": "unanimity", "G657": "undistracted", "G658": "unwaveringly", "G659": "unfit", "G660": "to cause to cease",
    "G661": "to reject", "G662": "worthless", "G663": "to crave", "G664": "eagerly anticipating", "G665": "expectation",
    "G666": "to look out for oneself", "G667": "to complete, i.e. accomplish", "G668": "to be perfect, i.e. complete", "G669": "apphia, a christian woman", "G670": "appius, a roman praenomen",
    "G671": "unapproachable", "G672": "intolerant", "G673": "unlearned, illiterate, i.e. unversed", "G674": "worthless", "G675": "a curse",
    "G676": "to curse", "G677": "a hook", "G678": "apprehension", "G679": "to begin to touch", "G680": "to attach oneself to",
    "G681": "to set on fire", "G682": "arabia, a region of asia", "G683": "an arabian or inhabitant of arabia", "G684": "an arabian", "G685": "aram, an israelite",
    "G686": "a spider", "G687": "a spider's web", "G688": "ploughing", "G689": "a plough", "G690": "to plough",
    "G691": "areopagus, a hill at athens", "G692": "an areopagite or member of the court held on ar...", "G693": "pleasing, agreeable", "G694": "agreeableness", "G695": "to be agreeable",
    "G696": "aretas, an arabian king", "G697": "goodness, virtue, excellence", "G698": "a male lamb", "G699": "number", "G700": "to number",
    "G701": "ariathous, a mountain", "G702": "arima-thaia, a place in palestine", "G703": "aristarchus, a macedonian", "G704": "to breakfast", "G705": "best",
    "G706": "aristoboulus, a christian", "G707": "the left hand or side", "G708": "sufficient", "G709": "to be sufficient", "G710": "sufficiency",
    "G711": "ares, the greek god of war", "G712": "arkas, a boat", "G713": "arkadios, a city", "G714": "arkesilas, a macedonian king", "G715": "an arkite",
    "G716": "a bear", "G717": "a chariot", "G718": "to equip", "G719": "harmodios, an athenian", "G720": "to join",
    "G721": "a joint", "G722": "to refuse", "G723": "a negative reply", "G724": "spoil", "G725": "a spoiler",
    "G726": "to seize", "G727": "rapacious", "G728": "a male", "G729": "newly planted", "G730": "newly planted",
    "G731": "unspeakable", "G732": "artemas, a christian", "G733": "to suspend", "G734": "artemis, the name of a greek goddess", "G735": "a foresail",
    "G736": "just now", "G737": "bread", "G738": "to fit", "G739": "artaxerxes, a persian king", "G740": "a loaf of bread",
    "G741": "arphaxad, a son of shem", "G742": "archangel", "G743": "archelaos, a macedonian king", "G744": "primitive", "G745": "a file leader",
    "G746": "beginning", "G747": "a captain", "G748": "a chief priest", "G749": "sacerdotal", "G750": "archippos, a christian",
    "G751": "chief shepherd", "G752": "to be first (in political rank or power)", "G753": "a custom-house", "G754": "a chief publican", "G755": "a ruler of a synagogue",
    "G756": "to set the table", "G757": "to rule", "G758": "a first, chief", "G759": "a chief butler", "G760": "a ruler",
    "G761": "fragrance", "G762": "asa, an israelite", "G763": "incorruptible", "G764": "incorruptibility", "G765": "uncertainty",
    "G766": "to be extinguished", "G767": "impious, ungodly", "G768": "to be impious", "G769": "impiety", "G770": "unmarked",
    "G771": "asher, an israelite", "G772": "weakness", "G773": "weakly", "G774": "to be weak", "G775": "weakness",
    "G776": "to banquet", "G777": "foodless", "G778": "asia", "G779": "an asian", "G780": "an asiarch",
    "G781": "unfed", "G782": "unskilled", "G783": "gladly", "G784": "a kiss", "G785": "unwise",
    "G786": "unwisely", "G787": "asp, a venomous serpent", "G788": "spotless", "G789": "a shield", "G790": "a star",
    "G791": "star-gazer", "G792": "star-shaped", "G793": "unsupported", "G794": "inconsistent", "G795": "lightning",
    "G796": "to flash lightning", "G797": "astrologer", "G798": "astronomy", "G799": "unsubmissive", "G800": "unnatural",
    "G801": "instability", "G802": "unstable", "G803": "security", "G804": "securely", "G805": "to make firm",
    "G806": "to gaze", "G807": "dishonor", "G808": "uncomely", "G809": "uncomeliness", "G810": "childless",
    "G811": "asynkritos, a roman christian", "G812": "uncompounded", "G813": "incoherent", "G814": "impatient", "G815": "impatience",
    "G816": "to gaze intently", "G817": "at the very time", "G818": "disorderly", "G819": "to be disorderly", "G820": "disorderly",
    "G821": "dishonor", "G822": "dishonorable", "G823": "to dishonor", "G824": "to be invisible", "G825": "invisible",
    "G826": "self-willed", "G827": "to shine", "G828": "day-break", "G829": "brightness", "G830": "dry",
    "G831": "a courtyard", "G832": "to lodge in the court-yard", "G833": "to play the flute", "G834": "a flute-player", "G835": "a flute",
    "G836": "strictly", "G837": "to increase", "G838": "increase", "G839": "self-condemned", "G840": "self-appointed",
    "G841": "spontaneous", "G842": "the very", "G843": "the same", "G844": "from the same spot", "G845": "in the same place",
    "G846": "self", "G847": "self-sufficient", "G848": "self-sufficiency", "G849": "self-taught", "G850": "self-evident",
    "G851": "removal", "G852": "separation", "G853": "aphphasia, a region of asia", "G854": "aphphasios, an inhabitant of aphphasia", "G855": "to send away",
    "G856": "to take away", "G857": "to take away", "G858": "unfruitful", "G859": "remission", "G860": "to go away",
    "G861": "to separate", "G862": "absence", "G863": "to send away", "G864": "unthankful", "G865": "unthankfulness",
    "G866": "to go away", "G867": "unapproachable", "G868": "to remove", "G869": "wormwood", "G870": "unfelt",
    "G871": "achaia, a region of greece", "G872": "achaian", "G873": "unthankful", "G874": "achaicus, a christian", "G875": "useless",
    "G876": "to render useless", "G877": "useless", "G878": "achilles, a greek hero", "G879": "mist", "G880": "unimpaired",
    "G881": "unhandy", "G882": "unhandy", "G883": "achmetha, the capital of media", "G884": "achbor, an israelite", "G885": "unprofitable",
    "G886": "unprofitableness", "G887": "acheron, a river in hades", "G888": "useless", "G889": "uselessness", "G890": "achzib, a place in palestine",
    "G891": "without ψεῦδος (falsehood)", "G892": "uncontaminated", "G893": "undying", "G894": "wormwood", "G895": "apsinthion, a star",
    "G896": "babilón, the capital of chaldæa", "G897": "deep", "G898": "to deepen", "G899": "depth", "G900": "bathos, a liquid measure",
    "G901": "a step", "G902": " βαθύς (deep)-rooted", "G903": "deep", "G904": " βαΐον (a palm twig)", "G905": "balaam, a prophet",
    "G906": "to throw", "G907": "to immerse, dip", "G908": "immersion, dipping", "G909": " βαπτισμός (immersion)", "G910": "a baptizer",
    "G911": "to baptize", "G912": "barabbas, an israelite", "G913": "barachias, an israelite", "G914": "barak, an israelite", "G915": "foreign",
    "G916": "heavily", "G917": "to burden", "G918": "barnabas, an israelite", "G919": "barsabas, the name of two israelites", "G920": "bartholomew, an apostle",
    "G921": "barjesus, an israelite", "G922": "bartimaeus, an israelite", "G923": "barys, a persian measure", "G924": " barytimos (highly valuable)", "G925": "to weigh down",
    "G926": "heavy", "G927": " βασανίζω (to torture)", "G928": "a touchstone (basanos), i.e. torture", "G929": " βασανισμός (torture)", "G930": " βασανιστής (a torturer)",
    "G931": " βάσις (a foot)", "G932": " βασιλεία (royalty)", "G933": " βασίλειον (a palace)", "G934": " βασίλειος (kingly)", "G935": "a king",
    "G936": "to be king", "G937": "kingly", "G938": "a queen", "G939": " βασκάνιος (malignant)", "G940": " βαστάζω (to lift)",
    "G941": " βάτος (a bramble-bush)", "G942": " βάτος (a bath or measure)", "G943": " βατραχος (a frog)", "G944": " βαττολογέω (to stutter)", "G945": " βδέλυγμα (a detestation)",
    "G946": " βδελυκτός (detestable)", "G947": " βδελύσσω (to stink)", "G948": " βέβαιος (stable)", "G949": " βεβαιόω (to stabilitate)", "G950": " βεβαίωσις (confirmation)",
    "G951": " βέβηλος (allowable to tread)", "G952": " βεβηλόω (to desecrate)", "G953": "beelzeboul, a name of satan", "G954": "belial, a name of satan", "G955": " βέλος (a missile)",
    "G956": " βελτίων (better)", "G957": "benjamin, an israelite", "G958": "bernice, a member of the herodian family", "G959": "beroia, a place in macedonia", "G960": "a beroean",
    "G961": "bethania, a place in palestine", "G962": "bethany", "G963": "bethabara, a place in palestine", "G964": "bethesda, a pool in jerusalem", "G965": "bethlehem, a place in palestine",
    "G966": "bethlehemite", "G967": "bethsaida, a place in palestine", "G968": " βῆμα (a step)", "G969": " βήρυλλος (beryl)", "G970": " βία (force)",
    "G971": " βιάζω (to force)", "G972": " βίαιος (violent)", "G973": " βιαστής (a forcer)", "G974": " βιβλαρίδιον (a booklet)", "G975": " βιβλίον (a roll)",
    "G976": " βίβλος (a scroll)", "G977": " βιβρώσκω (to eat)", "G978": "bithynia, a region of asia", "G979": " βίος (life)", "G980": " βιόω (to live)",
    "G981": " βίωσις (mode of life)", "G982": " βιωτικός (relating to life)", "G983": " βλαβερός (hurtful)", "G984": " βλάπτω (to hinder)", "G985": " βλαστάνω (to sprout)",
    "G986": " βλάστος (a sprout)", "G987": " βλασφημέω (to vilify)", "G988": " βλασφημία (vilification)", "G989": " βλάσφημος (vilifying)", "G990": " βλέμμα (sight)",
    "G991": " βλέπω (to look)", "G992": " βλητέος (meet to be cast)", "G993": "boanerges, a title given to two apostles", "G994": " βοάω (to halloo)", "G995": " βοή (a cry)",
    "G996": " βοήθεια (aid)", "G997": " βοηθέω (to aid)", "G998": " βοηθός (a helper)", "G999": " βόθυνος (a hole)", "G1000": " βολή (a throw)",
    "G1001": " βολίζω (to heave the lead)", "G1002": " βολίς (a missile)", "G1003": "boos, an israelite", "G1004": " βόρβορος (mud)", "G1005": " βορρᾶς (the north wind)",
    "G1006": " βόσκω (to feed)", "G1007": " βόσκημα (fodder)", "G1008": " βόσπορος (strait of the ox)", "G1009": " βοτάνη (herbage)", "G1010": " βότρυς (a bunch of grapes)",
    "G1011": " βουλεύτης (an adviser)", "G1012": " βουλεύω (to advise)", "G1013": " βουλή (volition)", "G1014": " βούλημα (a purpose)", "G1015": " βούλομαι (to \"will\")",
    "G1016": " βουνός (a hillock)", "G1017": " βους (an ox)", "G1018": " βραβεῖον (a prize)", "G1019": " βραβεύω (to arbitrate)", "G1020": " βραδύνω (to delay)",
    "G1021": " βραδυπλoέω (to sail slowly)", "G1022": " βραδύς (slow)", "G1023": " βραδύτης (slowness)", "G1024": " βραχίων (the arm)", "G1025": " βραχύς (short)",
    "G1026": " βρέφος (an infant)", "G1027": " βρέχω (to moisten)", "G1028": " βροντή (thunder)", "G1029": " βροχή (rain)", "G1030": " βρόχος (a noose)",
    "G1031": " βρύζω (to chew)", "G1032": " βρύω (to swell out)", "G1033": " βρῶμα (food)", "G1034": " βρώσιμος (eatable)", "G1035": " βρῶσις (eating)",
    "G1036": " βυθίζω (to sink)", "G1037": " βυθός (depth)", "G1038": " βυρσεύς (a tanner)", "G1039": " βύσσινος (of fine linen)", "G1040": " βύσσος (byssus)",
    "G1041": " βωμός (an elevation)", "G1042": " γάββαθα (gabbatha)", "G1043": "gabriel, an archangel", "G1044": " γάγγραινα (a gangrene)", "G1045": "gad, an israelite",
    "G1046": "a gadarene", "G1047": " γάδαρα (gadara)", "G1048": " γάζα (treasure)", "G1049": " γαζοφυλάκιον (a treasury)", "G1050": "gaius, a macedonian",
    "G1051": " γάλα (milk)", "G1052": "galatia, a region of asia", "G1053": "a galatian", "G1054": "galatian", "G1055": " γαλήνη (tranquillity)",
    "G1056": "galilee, a region of palestine", "G1057": "galilean", "G1058": "gallion, a roman proconsul", "G1059": " γαμέω (to marry)", "G1060": " γαμίζω (to give in marriage)",
    "G1061": " γάμος (marriage)", "G1062": " γάμος (wedding)", "G1063": " γάρ (for)", "G1064": " γαστήρ (the stomach)", "G1065": " γέ (at least)",
    "G1066": "gedeon, an israelite", "G1067": " γεεννα (gehenna)", "G1068": "gethsemane, a garden near jerusalem", "G1069": " γείτων (a neighbor)", "G1070": " γελάω (to laugh)",
    "G1071": " γέλως (laughter)", "G1072": " γεμίζω (to fill)", "G1073": " γέμω (to swell)", "G1074": " γενεά (generation)", "G1075": " γενεαλογέω (to trace lineage)",
    "G1076": " γενεαλογία (genealogy)", "G1077": " γενέσια (birthday celebrations)", "G1078": " γένεσις (nativity)", "G1079": " γενετή (birth)", "G1080": " γεννάω (to procreate)",
    "G1081": " γέννημα (offspring)", "G1082": "gennesaret, a lake and plain in palestine", "G1083": " γέννησις (nativity)", "G1084": " γεννητός (generated)", "G1085": " γένος (kin)",
    "G1086": " γερουσια (the eldership)", "G1087": " γέρων (aged)", "G1088": " γεύομαι (to taste)", "G1089": " γεωργέω (to till)", "G1090": " γεώργιον (cultivation)",
    "G1091": " γεωργός (a land-worker)", "G1092": " γεωργός (a farmer)", "G1093": " γῆ (soil)", "G1094": " γῆρας (old age)", "G1095": " γηράσκω (to become old)",
    "G1096": " γίνομαι (to become)", "G1097": " γινώσκω (to \"know\")", "G1098": " γλεῦκος (must)", "G1099": " γλυκύς (sweet)", "G1100": " γλῶσσα (the tongue)",
    "G1101": " γλωσσόκομον (a case)", "G1102": " γναφεύς (a fuller)", "G1103": " γνήσιος (legitimate)", "G1104": " γνησίως (genuinely)", "G1105": " γνόφος (gloom)",
    "G1106": " γνώμη (cognition)", "G1107": " γνωρίζω (to make known)", "G1108": " γνῶσις (knowing)", "G1109": " γνώστης (a knower)", "G1110": " γνωστός (known)",
    "G1111": " γογγύζω (to grumble)", "G1112": " γογγυσμός (a grumbling)", "G1113": " γογγυστής (a grumbler)", "G1114": " γόης (a wizard)", "G1115": "golgotha, a knoll near jerusalem",
    "G1116": "gomorrha, a place near the dead sea", "G1117": " γόμος (a load)", "G1118": " γονεύς (a parent)", "G1119": " γόνυ (the knee)", "G1120": " γονυπετέω (to fall on the knee)",
    "G1121": " γράμμα (a writing)", "G1122": " γραμματεύς (a writer)", "G1123": " γραπτός (written)", "G1124": " γραφή (a writing)", "G1125": " γράφω (to \"grave\")",
    "G1126": " γραώδης (old-wifely)", "G1127": " γρηγορέω (to keep awake)", "G1128": " γυμνάζω (to practise)","G1129": "γυμνασία (gymnasia, exercise)", "G1130": "γυμνάζω (gymnazō, to exercise)", "G1131": "γυμνίτης (gymnitēs, a runner)", "G1132": "γυμνητεύω (gymnēteuō, to be lightly clad)", "G1133": "γυμνός (gymnos, naked)", "G1134": "γυμνότης (gymnotēs, nakedness)", "G1135": "γυνή (gynē, a woman)", "G1136": "γυναικάριον (gynaikarion, a little woman)", "G1137": "γυναικεῖος (gynaikeios, female)", "G1138": "γυνή (gynē, a woman)", "G1139": "γυνή (gynē, a woman, wife)", "G1140": "γωνία (gōnia, a corner)", "G1141": "goph (an ape)", "G1142": "gutil (a bucket)", "G1143": "Δαβίδ (Dabid, David)", "G1144": "dabr (a word)", "G1145": "δαίμων (daimōn, a demon)", "G1146": "δαιμονίζομαι (daimonizomai, to be possessed by a demon)", "G1147": "δαιμονιώδης (daimoniōdēs, demoniacal)", "G1148": "δαιμόνιον (daimonion, a demon)", "G1149": "δαίμων (daimōn, a deity, demon)", "G1150": "δάκνω (daknō, to bite)", "G1151": "δάκρυ (dakry, a tear)", "G1152": "δακρύω (dakryō, to weep)","G1153": "δακτύλιος (daktylios, a ring)", "G1154": "δάκτυλος (daktylos, a finger)", "G1155": "δαλ (daleth)", "G1156": "Δαλμανουθά (Dalmanoutha)", "G1157": "Δαλματία (Dalmatia)", "G1158": "δαμάζω (damazō, to tame)", "G1159": "δάμαλις (damalis, a heifer)", "G1160": "Δάμαρις (Damaris)", "G1161": "Δαμασκηνός (Damaskēnos, of Damascus)", "G1162": "Δαμασκός (Damaskos, Damascus)", "G1163": "δανείζω (daneizō, to lend)", "G1164": "δάνειον (daneion, a debt)", "G1165": "δανειστής (daneistēs, a lender)", "G1166": "Δανιήλ (Daniēl, Daniel)", "G1167": "δάπανα (dapana, cost)", "G1168": "δαπανάω (dapanaō, to spend)", "G1169": "δέ (de, but, and)", "G1170": "δέησις (deēsis, prayer)", "G1171": "δεητός (deētos, prayed for)", "G1172": "δέομαι (deomai, to pray)", "G1173": "δεῖ (dei, it is necessary)", "G1174": "δεῖγμα (deigma, a sample)", "G1175": "δειγματίζω (deigmatizō, to make a show of)", "G1176": "δείκνυμι (deiknymi, to show)", "G1177": "δειλία (deilia, cowardice)", "G1178": "δειλιάω (deiliaō, to be cowardly)", "G1179": "δειλός (deilos, cowardly)", "G1180": "δεῖνα (deina, such a one)", "G1181": "δεινῶς (deinōs, terribly)", "G1182": "δειπνέω (deipneō, to dine)",  "G1183": "δεῖπνον (deipnon, a supper)", "G1184": "δεισιδαιμονία (deisidaimonia, religion)", "G1185": "δεισιδαίμων (deisidaimōn, religious)", "G1186": "δέκα (deka, ten)", "G1187": "δεκαδύο (dekadyo, twelve)", "G1188": "δεκαπέντε (dekapente, fifteen)", "G1189": "Δεκάπολις (Dekapolis, Decapolis)", "G1190": "δέκατος (dekatos, tenth)", "G1191": "δεκατέσσαρες (dekatessares, fourteen)", "G1192": "δεκάτη (dekatē, a tenth)", "G1193": "δεκατόω (dekatoō, to pay tithes)", "G1194": "δεκτός (dektos, acceptable)", "G1195": "δελεάζω (deleazō, to lure)", "G1196": "δέλτος (deltos, a writing tablet)", "G1197": "δένδρον (dendron, a tree)", "G1198": "δεξιολάβος (dexiolabos, a spearman)", "G1199": "δεξιός (dexios, right)", "G1200": "δέον (deon, that which is needful)", "2424": " Ἰησοῦς (Iésous)",
# --- Batch G1250-G1300 ---
'G1250': 'diakosioi; from dis and hekaton; two hundred: - two hundred.',
'G1251': 'diakouomai; middle voice from dia and akouo; to hear throughout, i.e. patiently listen (to a prisoners plea): - hear.',
'G1252': 'diakrino; from dia and krino; to separate thoroughly, i.e. (literally and reflexively) to withdraw from, or (by implication) oppose; figuratively, to discriminate (by implication, decide), or (reflexively) hesitate: - contend, make (to) differ(-ence), discern, doubt, judge, be partial, stagger, waver.',
'G1253': 'diakrisis; from diakrino; judicial estimation: - discern(-ing), disputation.',
'G1254': 'dialaleo; from dia and laleo; to talk throughout a company, i.e. converse or (genitive case) publish: - commune, noise abroad.',
'G1255': 'dialektos; from dialegomai; a (mode of) discourse, i.e. dialect: - language, tongue.',
'G1256': 'dialegomai; middle voice from dia and lego; to say thoroughly, i.e. discuss (in argument or exhortation): - dispute, preach (unto), reason (with), speak.',
'G1257': 'dialeipo; from dia and leipo; to leave off, i.e. intermit: - cease.',
'G1258': 'diallasso; from dia and allasso; to change thoroughly, i.e. (mentally) to conciliate: - reconcile.',
'G1259': 'dialogizomai; from dia and logizomai; to reckon thoroughly, i.e. (genitive case) to deliberate (by reflection or discussion): - cast in mind, consider, dispute, muse, reason, think.',
'G1260': 'dialogismos; from dialogizomai; discussion, i.e. (internal) consideration (by implication, purpose), or (external) debate: - dispute, doubtful(-ing), imagination, reasoning, thought.',
'G1261': 'dialoidoreo; from dia and loidoreo; to rail vehemently: - revile again.',
'G1262': 'dialuo; from dia and luo; to dissolve utterly: - scatter.',
'G1263': 'diamarturomai; from dia and marturomai; to attest or protest earnestly, or (by implication) hortatively: - charge, testify (unto), witness.',
'G1264': 'diamachomai; from dia and machomai; to fight fiercely (in altercation): - strive.',
'G1265': 'diameno; from dia and meno; to stay constantly (in being or relation): - continue, remain.',
'G1266': 'diamerizo; from dia and merizo; to partition thoroughly (literally in distribution, figuratively in dissension): - cloven, divide, part.',
'G1267': 'diamerismos; from diamerizo; disunion (of opinion and conduct): - division.',
'G1268': 'dianemo; from dia and the base of nomos; to distribute, i.e. (of information) to disseminate: - spread.',
'G1269': 'dianeuo; from dia and neuo; to nod (or express by signs) across an intervening space: - beckon.',
'G1270': 'dianoema; from a compound of dia and noeo; something thought through, i.e. a sentiment: - thought.',
'G1271': 'dianoia; from dia and nous; deep thought, properly, the faculty (mind or its disposition), by implication, its exercise: - imagination, mind, understanding.',
'G1272': 'dianoigo; from dia and anoigo; to open thoroughly, literally (as a first-born) or figuratively (to expound): - open.',
'G1273': 'dianuktereuo; from dia and a derivative of nux; to sit up the whole night: - continue all night.',
'G1274': 'dianuo; from dia and anuo (to effect); to accomplish thoroughly: - finish.',
'G1275': 'diapantos; from dia and the genitive case of pas; through all time, i.e. (adverbially) constantly: - alway(-s), continually.',
'G1276': 'diaperao; from dia and a derivative of the base of peran; to cross entirely: - go over, pass (over), sail over.',
'G1277': 'diapleo; from dia and pleo; to sail through: - sail over.',
'G1278': 'diaponeo; from dia and a derivative of ponos; to toil through, i.e. (passively) be worried: - be grieved.',
'G1279': 'diaporeuomai; from dia and poreuomai; to travel through: - go through, journey in, pass by.',
'G1280': 'diaporeo; from dia and aporeo; to be thoroughly nonplussed: - (be in) doubt, be (much) perplexed.',
'G1281': 'diapragmateuomai; from dia and pragmateuomai; to thoroughly occupy oneself, i.e. (transitively and by implication) to earn in business: - gain by trading.',
'G1282': 'diaprio; from dia and prio (to saw); to saw asunder, i.e. (figuratively) to exasperate: - cut (to the heart).',
'G1283': 'diarpazo; from dia and harpazo; to seize asunder, i.e. plunder: - spoil.',
'G1284': 'diarrhesso; from dia and rhesso; to tear asunder: - break, rend.',
'G1285': 'di asapheo; from dia and saphes (clear); to clear thoroughly, i.e. (figuratively) declare: - tell unto.',
'G1286': 'diaseio; from dia and seio; to shake thoroughly, i.e. (figuratively) to intimidate: - do violence to.',
'G1287': 'diaskorpizo; from dia and skorpizo; to scatter abroad, i.e. dissipate; figuratively, to squander: - disperse, scatter (abroad), strew, waste.',
'G1288': 'diaspao; from dia and spao; to draw apart, i.e. sever or dismember: - pluck asunder, pull in pieces.',
'G1289': 'diaspeiro; from dia and speiro; to sow throughout, i.e. (figuratively) distribute in foreign lands: - scatter abroad.',
'G1290': 'diaspora; from diaspeiro; dispersion, i.e. (specially and concretely) the (converted) Israelite resident in Gentile countries: - (which are) scattered (abroad).',
'G1291': 'diastellomai; middle voice from dia and stello; to set (oneself) apart (figuratively, distinguish), i.e. (by implication) to enjoin: - charge, that which was (give) commanded(-ment).',
'G1292': 'diastema; from diistemi; an interval: - space.',
'G1293': 'diastole; from diastellomai; a variation: - difference, distinction.',
'G1294': 'diastrepho; from dia and strepho; to distort, i.e. (figuratively) misinterpret, or (morally) corrupt: - perverse, pervert, turn away.',
'G1295': 'diasozo; from dia and sozo; to save thoroughly, i.e. (by implication or analogy) to cure, preserve, rescue, etc.: - bring safe, escape (safe), heal, make perfectly whole, save.',
'G1296': 'diatage; from diatasso; arrangement, i.e. institution: - disposition.',
'G1297': 'diatagma; from diatasso; an arrangement, i.e. (authoritative) edict: - commandment.',
'G1298': 'diatarasso; from dia and tarasso; to disturb wholly, i.e. agitate (with alarm): - trouble.',
'G1299': 'diatasso; from dia and tasso; to arrange thoroughly, i.e. (specially) institute, prescribe, etc.: - appoint, command, give, (set in) order, ordain.',
'G1300': 'diateleo; from dia and teleo; to accomplish thoroughly, i.e. (subjectively) to persist: - continue.',# --- Batch G1301-G1400 ---
'G1301': 'diatereo; from dia and tereo; to keep through (in every part), i.e. (figuratively) to observe strictly: - keep.',
'G1302': 'diati; from dia and tis; through what cause?, i.e. why?: - wherefore, why.',
'G1303': 'diatithemai; middle voice from dia and tithemi; to put apart, i.e. (figuratively) dispose (by assignment, compact or bequest): - appoint, make, testator.',
'G1304': 'diatribe; from a compound of dia and tribo; a tarrying, i.e. residence: - X abide, + pass the time.',
'G1305': 'diatribo; from dia and tribo; to wear through (time), i.e. remain, delay: - abide, be, continue, tarry.',
'G1306': 'diatrophe; from a compound of dia and trepho; nourishment: - food.',
'G1307': 'diaugazo; from dia and augazo; to shine through, i.e. become obvious: - dawn.',
'G1308': 'diaphanes; from dia and phaino; appearing through, i.e. diaphanous: - transparent.',
'G1309': 'diaphero; from dia and phero; to bear through, i.e. (literally) transport; usually, to differ (i.e. be superior); subjectively, to be uncertain (in dispute); objectively, to be important: - be better, carry, differ from, drive up and down, be excellent, make matter, publish, be of more value.',
'G1310': 'diapheugo; from dia and pheugo; to flee through, i.e. escape: - escape.',
'G1311': 'diaphemizo; from dia and a derivative of phemi; to report different ways, i.e. circulate publicy: - blaze abroad, commonly (report), spread abroad, fame.',
'G1312': 'diaphtheiro; from dia and phtheiro; to rot thoroughly, i.e. (by implication) to ruin (passively, decay): - corrupt, destroy, perish.',
'G1313': 'diaphthora; from diaphtheiro; decay: - corruption.',
'G1314': 'diaphoros; from diaphero; variable, i.e. different; by implication, superior: - differ(-ing), diverse, more excellent.',
'G1315': 'diaphulasso; from dia and phulasso; to guard thoroughly, i.e. (by implication) to protect: - keep.',
'G1316': 'diacheirizo; from dia and a derivative of cheir; to handle thoroughly, i.e. (by implication) lay violent hands on: - kill, slay.',
'G1317': 'diachorizomai; middle voice from dia and chorizo; to separate entirely: - depart.',
'G1318': 'didaktikos; from didasko; instructive: - apt to teach.',
'G1319': 'didaskalia; from didaskalos; instruction (the function or the information): - doctrine, learning, teaching.',
'G1320': 'didaskalos; from didasko; an instructor (genitive case or specially): - doctor, master, teacher.',
'G1321': 'didasko; a prolonged (causative) form of a primary verb dao (to learn); to teach (in the same broad application): - teach.',
'G1322': 'didache; from didasko; instruction (the act or the matter): - doctrine, hath been taught, teaching.',
'G1Next': 'didrachmon; from dis and drachme; a double drachma (tax): - tribute.',
'G1324': 'Didumos; from dis; twofold, i.e. twin; Didymus, a name for Thomas: - Didymus.',
'G1325': 'didomi; a prolonged form of a primary verb (which is used as an alternative in most of the tenses); to give (used in a very wide application, properly, or by implication, literally or figuratively; greatly modified by the connection): - adventure, bestow, bring forth, commit, deliver (up), give, grant, hinder, make, minister, number, offer, have power, put, receive, set, shew, smite (+ with the hand), strike (+ with the palm of the hand), suffer, take, utter, yield.',
'G1326': 'diegeiro; from dia and egeiro; to wake up thoroughly; i.e. (figuratively) to rouse (from sleep, from sitting, from obscurity, from inaction): - arise, awake, raise, stir up.',
'G1327': 'diegesis; from diegeomai; a recital: - declaration.',
'G1Three': 'diegeomai; middle voice from dia and hegeomai; to relate fully: - declare, shew, tell.',
'G1329': 'diegersis; from diegeiro; arousal: - awaking.',
'G1330': 'diermeneutes; from diermeneuo; a translator: - interpreter.',
'G1331': 'diermeneuo; from dia and hermeneuo; to interpret fully, i.e. (by implication) to translate: - expound, interpret(-ation).',
'G1332': 'dierchomai; from dia and erchomai; to traverse (literally): - come, depart, go (abroad, about, every way, into, over, through, throughout), pass (by, over, through, throughout), pierce through, travel, walk through.',
'G1333': 'dierotao; from dia and erotao; to question through, i.e. ascertain by search: - make enquiry for.',
'G1334': 'dietes; from dis and etos; of two years: - two years old.',
'G1335': 'dietia; from dietes; a two-year period: - two years.',
'G1336': 'digamos; from dis and gamos; twice married: - have two husbands.',
'G1Example': 'dike; probably a prime word; right (as self-evident), i.e. justice (the principle, a decision, or its execution): - judgment, punish, vengeance.',
'G1338': 'diktuon; probably from a primitive dikein (to cast); a seine (for fishing): - net.',
'G1339': 'dikaiokrisia; from dikaios and krisis; a just sentence: - righteous judgment.',
'G1340': 'dikaios; from dike; equitable (in character or act); by implication, innocent, holy (absolutely or relatively): - just, meet, right(-eous).',
'G1341': 'dikaiosune; from dikaios; equity (of character or act); specially (Christian) justification: - justification, righteousness.',
'G1342': 'dikaioo; from dikaios; to render (i.Define'  'dikaioma; from dikaioo; an equitable deed; by implication, a statute or decision: - judgment, justification, ordinance righteousness.',
'G1344': 'dikaios; adverb from dikaios; equitably: - justly, (to) right(-eously).',
'G1345': 'dikastes; from a derivative of dike; a judge: - judge.',
'G1346': 'dilogos; from dis and logos; equivocal, i.e. double-tongued: - double-tongued.',
'G1347': 'dio; from dia and hos; through which thing, i.e. consequently: - for which cause, therefore, wherefore.',
'G1348': 'diodeuo; from dia and hodeuo; to travel through: - go through, pass through.',
'G1349': 'Diopetes; from the alternate of Zeus and the base of pipto; sky-fallen (i.e. an aerolite): - which fell down from Jupiter.',
'G1350': 'diorthoma; from a compound of dia and orthoo (to straighten); something rectified, i.e. (figuratively) reformation: - reformation.',
'G1351': 'diorthosis; from the same as diorthoma; rectification: - reformation.',
'G1352': 'diorusso; from dia and orusso; to dig through: - break through (up).',
'G1353': 'dis; adverb from duo; twice: - again, twice.',
'G1354': 'distazo; from dis; properly, to duplicate, i.e. (mentally) to waver (in opinion): - doubt.',
'G1355': 'distomos; from dis and stoma; double-edged: - with two edges.',
'G1356': 'dischilioi; from dis and chilioi; two thousand: - two thousand.',
'G1357': 'diistemi; from dia and histemi; to stand apart, i.e. intervene, or (partitively) to differ: - be between, part.',
'G1358': 'diischurizomai; from dia and ischuromai; to stoutly affirm: - constantly affirm.',
'G1359': 'Dios; from Dios; of Jove, i.e. (in the genitive case) the day of Jupiter (Thursday): - Thursday.',
'G1360': 'dioti; from dio and hoti; on the very account that, or inasmuch as: - because, for, therefore.',
'G1361': 'Diotrephes; from a compound of the alternate of Zeus and trepho (to rear); Jove-nourished; Diotrephes, an opponent of Christianity: - Diotrephes.',
'G1362': 'diplous; from dis and (a form of) ploos (fold); two-fold: - double, two-fold more.',
'G1363': 'diploo; from diplous; to render twofold: - double.',
'G1364': 'dis; from duo; twice: - again, double.',
'G1365': 'dis; from duo; two: - two.',
'G1366': 'dipsao; from a variation of dipsos; to thirst for (literally or figuratively): - (be, suffer) thirst(-y).',
'G1367': 'dipsos; of uncertain affinity; thirst: - thirst.',
'G1368': 'dipsuchos; from dis and psuche; two-spirited, i.e. wavering (in opinion or purpose): - double-minded.',
'G1369': 'dogma; from the base of dokeo; a law (civil, ceremonial or ecclesiastical): - decree, ordinance.',
'G1370': 'dogmatizo; from dogma; to prescribe by statute, i.e. (reflexively) to submit to an ordinance: - be subject to ordinances.',
'G1371': 'dokeo; a prolonged form of a primary verb (used as an alternative of doko) of the same meaning; to think; by implication, to seem (right, good, etc.), i.e. suppose (intransitively, or transitively): - be accounted, be conclusive, be reputed, seem (good), suppose, think, trow.',
'G1372': 'dokimazo; from dokimos; to test (literally or figuratively); by implication, to approve: - allow, approve, discern, examine, like, prove, try.',
'G1Next': 'dokime; from dokimos; test (abstractly or concretely); by implication, trustiness: - experience(-riment), proof, trial.',
'G1374': 'dokimion; from dokimos; a testing; by implication, a test: - trial, trying.',
'G1375': 'dokimos; from dechomai; properly, acceptable (current after assay), i.e. approved: - approved, tried.',
'G1376': 'dokos; from dechomai (in the sense of holding up); a stick of timber: - beam.',
'G1377': 'dolios; from dolos; guileful: - deceitful.',
'G1378': 'dolioo; from dolios; to use deceit: - use deceit.',
'G1379': 'dolos; from an obsolete primary verb, dello (probably meaning to decoy); a trick (bait), i.e. (figuratively) wile: - craft, deceit, guile, subtilty.',
'G1380': 'doloo; from dolos; to ENSNARE, i.e. (figuratively) adulterate: - handle deceitfully.',
'G1381': 'doloma; from doloo; a trapan: - deceit.',
'G1382': 'doma; from the base of didomi; a gift: - gift.',
'G1383': 'doxa; from the base of dokeo; glory (as an appearance), i.e. (especially) splendor; figuratively, dignity, honor, praise, worship: - dignity, glory(-ious), honour, praise, worship.',
'G1384': 'doxazo; from doxa; to render (or esteem) glorious (in a wide application): - (make) glorious, glorify, honour, magnify.',
'G1385': 'Dorkas; gazelle; Dorcas, a Christian woman: - Dorcas.',
'G1386': 'dosis; from the base of didomi; a giving; by implication, (concretely) a gift: - gift, giving.',
'G1387': 'dotes; from the base of didomi; a giver: - giver.',
'G1388': 'douleia; from douleuo; slavery (literally or figuratively, involuntary or voluntary): - bondage.',
'G1389': 'douleuo; from doulos; to be a slave to (literal or figurative, voluntary or involuntary): - be in bondage, (do) serve(-ice), be a servant.',
'G1390': 'doule; feminine of doulos; a female slave (involuntary or voluntary): - handmaid(-en).',
'G1391': 'doulos; from deo; a slave (literal or figurative, involuntary or voluntary; frequently, therefore, in a qualified sense of subjection or submissiveness): - bond(-man), servant.',
'G1392': 'douloo; from doulos; to enslave (literally or figuratively): - bring into (be under) bondage, X given, become servant, serve.',
'G1Next': 'doche; from dechomai; a reception, i.e. a banquet: - feast.',
'G1394': 'drakon; from an assumed derivative of derkomai (to see); a fabulous kind of serpent (perhaps as supposed to fascinate): - dragon.',
'G1395': 'drassomai; perhaps identical with the base of drakon (through the idea of capturing); to grasp, i.Example'  'drachme; from drassomai; a drachma (a Greek coin): - piece (of silver).',
'G1397': 'dremo; a prolonged form of an obsolete primary verb; to run: - run.',
'G1398': 'drepanon; from drepo (to pluck); a sickle: - sickle.',
'G1399': 'dromos; from the alternate of trecho; a race, i.e. (figuratively) career: - course.',
'G1400': 'Drousilla; a feminine diminutive of Drusus (a Roman name); Drusilla, a member of the Herodian family: - Drusilla.',# --- Batch G1401-G1500 ---
'G1401': 'dunamis; from dunamai; force (literally or figuratively); specially, miraculous power (usually by implication, a miracle itself): - ability, abundance, meaning, might(-ily, -y, -y deed), (worker of) miracle(-s), power, strength, violence, mighty (wonderful) work.',
'G1Example': 'dunamoo; from dunamis; to enable: - strengthen.',
'G1403': 'dunastes; from dunamis; a ruler or officer: - mighty, potentate.',
'G1404': 'dunateo; from dunatos; to be efficient (in act or word): - be mighty, be (able), be strong.',
'G1405': 'dunatos; from dunamai; powerful or capable (literally or figuratively); neuter possible: - able, could, (that is) mighty (man), possible, power, strong.',
'G1406': 'duno; (in duplicate) dumi; prolonged forms of duo (to sink); to go down: - set.',
'G1407': 'duo; a primary numeral; two: - both, twain, two.',
'G1408': 'dus; a primary particle; difficult: - hard.',
'G1409': 'dusbastaktos; from dus and a derivative of bastazo; hard to be borne: - grievous to be borne.',
'G1410': 'dusenterion; from dus and a derivative of entos (meaning bowels); a malady of the bowels, i.e. dysentery: - bloody flux.',
'G1411': 'dusermeneutos; from dus and a derivative of hermeneuo; hard to set forth: - hard to be uttered.',
'G1412': 'duskolos; from dus and kolon (food); ill-fed, i.e. (by implication) fastidious (captious): - hard.',
'G1413': 'duskolos; adverb from duskolos; impracticably: - hardly.',
'G1414': 'dusme; from duno; the setting (of the sun), i.e. (by implication) the west: - west.',
'G1415': 'dusnoetos; from dus and a derivative of noeo; hard to be comprehended: - hard to be understood.',
'G1416': 'dusphemia; from a compound of dus and phemi; defamation: - evil report.',
'G1Note': 'dodeka; from duo and deka; two and ten, i.e. twelve: - twelve.',
'G1418': 'dodekatos; from dodeka; the twelfth: - twelfth.',
'G1419': 'dodekaphulon; from dodeka and phule; the twelve tribes (of Israel): - twelve tribes.',
'G1420': 'doma; from demo (to build); a building (properly, the roof or upper story, as being the most conspicuous part): - housetop.',
'G1421': 'dorea; from doron; a gratuity: - gift.',
'G1422': 'dorean; accusative case of dorea as adverb; gratuitously (literally or figuratively): - without a cause, freely, for nought, in vain.',
'G1423': 'doreomai; middle voice from dorea; to bestow gratuitously: - give.',
'G1424': 'dorema; from doreomai; a bestowment: - gift.',
'G1425': 'doron; a present; specially, a sacrifice: - gift, offering.',
'G1426': 'dosis; from the base of didomi; a giving; by implication, (concretely) a gift: - gift, giving.',
'G1427': 'dotes; from the base of didomi; a giver: - giver.',
'G1428': 'e; a primary particle of distinction between two connected terms; either, or, than: - either, or (else), than.',
'G1429': 'ea; imperative of eao (to let); properly, let it be, i.e. (as interjection) aha!: - ah, let alone.',
'G1430': 'eao; of uncertain affinity; to let be, i.e. permit or leave alone: - alone, leave, let (alone), suffer.',
'G1431': 'ebdomas; from heptas; a week: - week.',
'G1432': 'ebdomekonta; from heptas and deka; seventy: - seventy, three score and ten.',
'G1References': 'ebdomekontakis; multiple adverb from hebdomekonta; seventy times: - seventy times.',
'G1434': 'ebdomos; from heptas; the seventh: - seventh.',
'G1435': 'Eber; of Hebrew origin (H5677); Eber, a patriarch: - Eber.',
'G1436': 'Hebraikos; from Hebraisti; Hebraic, i.e. (specifically) the original forum of the Jewish language: - Hebrew.',
'G1437': 'Hebraios; from Eber; a Hebr?an (i.e. Hebrew) or descendant of Eber: - Hebrew.',
'G1438': 'Hebraisti; adverb from Hebraios; Hebraistically or in the Hebrew language: - in (the) Hebrew (tongue)..',
'G1439': 'Hebraikos; from Hebraios; Hebraic, i.e. (specifically) the original forum of the Jewish language: - Hebrew.',
'G1440': 'Hebraisti; adverb from Hebraios; Hebraistically or in the Hebrew language: - in (the) Hebrew (tongue).',
'G1441': 'Hebraios; from Eber; a Hebr?an (i.e. Hebrew) or descendant of Eber: - Hebrew.',
'G1442': 'Hebraisti; adverb from Hebraios; Hebraistically or in the Hebrew language: - in (the) Hebrew (tongue).',
'G1443': 'eggizo; from eggus; to make near, i.e. (reflexively) approach: - approach, be at hand, come (draw) near, be nigh.',
'G1444': 'eggrapho; from en and grapho; to enscribe (figuratively): - write (in).',
'G1445': 'egguos; from eggus (in the sense of joining); a bondsman: - surety.',
'G1446': 'eggus; from a primary verb agcho (to squeeze or throttle; akin to the base of agkale); near (literally or figuratively, of place or time): - from, at hand, near, nigh (at hand, unto), ready.',
'G1447': 'egguteron; neuter of the comparative of eggus; nearer: - nearer.',
'G1448': 'egeiro; probably akin to the base of agora (through the idea of collecting ones faculties); to waken (transitively or intransitively), i.e. rouse (literally, from sleep, from sitting or lying, from disease, from death; or figuratively, from obscurity, inactivity, ruins, nonexistence): - arise, lift (up), raise (again, up), rear up, (a-)wake.',
'G1449': 'egersis; from egeiro; a resurgence (from death): - resurrection.',
'G1450': 'egkainia; from a compound of en and kainos; renewals, i.e. (specially) an annual feast in commemoration of the re-dedication of the temple: - dedication.',
'G1451': 'egkainizo; from the same as egkainia; to renew, i.e. inaugurate: - consecrate, dedicate.',
'G1452': 'egkaleo; from en and kaleo; to call in (as a debt or demand), i.e. to accuse: - accuse, call in question, implead.',
'G1453': 'egkathetos; from en and a derivative of kathiemi; one put in, i.e. a secret emissary: - spy.',
'G1454': 'egkathizo; from en and kathizo; to seat in: - set in.',
'G1455': 'egkatoikeo; from en and katoikeo; to settle down in a place, i.e. reside: - dwell among.',
'G1456': 'egkentrizo; from en and kentron; to prick in, i.e. ingraft: - graff in(-to).',
'G1457': 'egklema; from egkaleo; an accusation, i.e. charge of crime: - crime laid against, charge.',
'G1458': 'egkomboomai; from en and komboo (to gird); to engirdle oneself (with an apron), i.e. (figuratively) to invest with: - be clothed.',
'G1459': 'egkope; from egkopto; a hindrance: - X hinder.',
'G1460': 'egkopto; from en and kopto; to cut into, i.e. (figuratively) impede, detain: - hinder, be tedious unto.',
'G1461': 'egkrateia; from egkrates; self-control (especially continence): - temperance.',
'G1462': 'egkrateuomai; middle voice from egkrates; to exercise self-control (in diet and chastity): - can(-not) contain, be temperate.',
'G1463': 'egkrates; from en and kratos; strong in a thing (masterful), i.e. (figuratively) self-controlled (in appetite, etc.): - temperate.',
'G1464': 'egkrino; from en and krino; to judge in, i.e. count among: - make of the number.',
'G1465': 'egkrupto; from en and krupto; to conceal in, i.e. incorporate with: - hid in.',
'G1466': 'egkuos; from en and the base of kuma; swelling (in the belly), i.e. pregnant: - great with child.',
'G1467': 'egchrio; from en and chrio; to rub in: - anoint.',
'G1468': 'ego; a primary pronoun of the first person I (only expressed when emphatic): - I, me.',
'G1469': 'edaphizo; from edaphos; to raze: - dash to the ground.',
'G1470': 'edaphos; from the base of hedraios; a basis (bottom), i.e. the ground: - ground.',
'G1471': 'hedraios; from a derivative of hezomai (to sit); sedentary, i.e. (by implication) immovable: - settled, stedfast.',
'G1472': 'hedraioma; from hedraios; a support, i.e. (figuratively) basis: - ground.',
'G1473': 'ego; a primary pronoun of the first person I (only expressed when emphatic): - I, me.',
'G1474': 'ezomai; a prolonged form of a primary verb hedo (to sit); to sit: - sit.',
'G1475': 'ethelo; or thelo; in certain tenses theleo or theleo; apparently strengthened from the alternate of haireomai; to determine (as an active choice), i.e. wish (implying volition, desire, or inclination): - be disposed, be glad, intend, list, love, mean, please, have rather, will (willing, willingly).',
'G1476': 'ethizo; from ethos; to accustom, i.e. (neuter passive participle) customary: - custom.',
'G1477': 'ethnikos; from ethnos; national (heathen, i.e. Gentile): - heathen (man).',
'G1478': 'ethnikos; adverb from ethnos; as a Gentile: - after the manner of Gentiles.',
'G1Examples': 'ethnos; probably from etho; a race (as of the same habit), i.e. a tribe; specially, a foreign (non-Jewish) one (usually by implication, pagan): - Gentile, heathen, nation, people.',
'G1480': 'ethos; from etho; a usage (prescribed by habit or law): - custom, manner, be wont.',
'G1481': 'etho; a primary verb; to be used (by habit or convention); neuter perfect participle customary: - custom, (be) wont.',
'G1482': 'ei; a primary particle of conditionality; if, whether, that, etc.: - albeit, because, whether, if, that, though, whether.',
'G1483': 'ei; a primary particle, used as subjunctive of eimi; if: - if.',
'G1484': 'ei; a primary particle, used as subjunctive of eimi; if: - if.',
'G1485': 'eido; a primary verb; used only in certain past tenses, the others being borrowed from the equivalent ginosko and horao; properly, to see (literally or figuratively); by implication, (in the perfect tense only) to know: - be aware, behold, X can (+ not tell), consider, (have) know(-ledge), look (on), perceive, see, be sure, tell, understand, wish, wot.',
'G1Details': 'eidos; from eido; a view, i.e. form (literally or figuratively): - appearance, fashion, shape, sight.',
'G1487': 'ei de me (ge); from ei, de and me (with ge); but if not: - otherwise.',
'G1488': 'eithe; from ei and the (sometimes unexpressed) optative of tis; oh that!: - would (to God).',
'G1489': 'ei kai; from ei and kai; if also (or even): - if (that), yea though.',
'G1Sure': 'ei me; from ei and me; if not: - but, except, if not, saving.',
'G1491': 'eimi; a prolonged form of a primary verb (used only in the present and imperfect tenses; the others being supplied by a kindred (middle voice) verb, ginomai, which see, or (in the infinitive) by a form, esomai, from a primary es-); to be (i.e. exist or live): - am, are, be(-long), have, is, need, pass, + remain, stand, was, etc.',
'G1492': 'eimi; from ei (a conditional particle); if: - if.',
'G1493': 'einai; present infinitive from eimi; to exist: - am, are, be(-long), + have, is, was, were.',
'G1494': 'ei per; from ei and per; if perhaps: - if so be (that), if yet.',
'G1495': 'ei pos; from ei and pos; if somehow: - if by any means',
'G1496': 'eireneuo; from eirene; to be (act) peaceable: - be at (have, live in) peace, live peaceably',
# --- Batch G1497-G1800 (Simple Format w/ Meaning) ---
'G1497': 'peace (well being)',
'G1498': 'eirenikos (peaceable)',
'G1499': 'eirenopoieo (to make peace)',
'G1500': 'eirenopoios (peacemaker)',
'G1501': 'eiro (to say, speak)',
'G1502': 'eis (into, in, among)',
'G1503': 'eis (one)',
'G1504': 'eisago (to bring in)',
'G1505': 'eisakouo (to hear, listen to)',
'G1506': 'eiserchomai (to go in, enter)',
'G1507': 'eisi (are)',
'G1508': 'eisin (they are)',
'G1509': 'eision (to enter)',
'G1510': 'eimi (to be, exist)',
'G1511': 'einai (to be)',
'G1512': 'eiper (if perhaps)',
'G1513': 'eipo (to say, speak)',
'G1514': 'eireo (to say, speak)',
'G1515': 'eisodos (an entrance, way in)',
'G1516': 'eisporeuomai (to go in, enter)',
'G1517': 'eistrecho (to run in)',
'G1518': 'eisphero (to bring in)',
'G1519': 'eis (into, to)',
'G1520': 'heis (one)',
'G1521': 'eischeo (to rush in)',
'G1522': 'eiso (within, inside)',
'G1523': 'eisotheo (to push in)',
'G1524': 'eita (then, next)',
'G1525': 'eite (if, whether)',
'G1526': 'eimi (I am)',
'G1527': 'ei tis (if anyone)',
'G1528': 'eio (to be accustomed)',
'G1529': 'eitho (to be accustomed)',
'G1530': 'eiotos (customary)',
'G1531': 'ei (if)',
'G1532': 'ek (from, out of)',
'G1533': 'ek (out of, from)',
'G1534': 'hekaton (a hundred)',
'G1535': 'eisphero (to bring in)',
'G1536': 'eita (then)',
'G1537': 'ek (out of, from)',
'G1538': 'hekastos (each, every)',
'G1539': 'hekastote (always)',
'G1540': 'hekaton (one hundred)',
'G1541': 'hekatontaplasion (a hundredfold)',
'G1542': 'hekatontarches (centurion)',
'G1543': 'hekatontarchos (centurion)',
'G1544': 'ekbaino (to go out)',
'G1545': 'ekballo (to cast out, send out)',
'G1546': 'ekbasis (an exit, outcome)',
'G1547': 'ekbole (a throwing out, cargo)',
'G1548': 'ekgameo (to marry, give in marriage)',
'G1549': 'ekgamisko (to give in marriage)',
'G1550': 'ekgonon (offspring, grandchild)',
'G1551': 'ekdapanao (to spend entirely)',
'G1552': 'ekdechomai (to expect, wait for)',
'G1553': 'ekdelos (very clear, evident)',
'G1554': 'ekdemeo (to be absent, away)',
'G1555': 'ekdidomi (to let out, lease)',
'G1556': 'ekdiegeomai (to relate in detail)',
'G1557': 'ekdikeo (to avenge, punish)',
'G1558': 'ekdikesis (vengeance, punishment)',
'G1559': 'ekdikos (avenger, punisher)',
'G1560': 'ekdioko (to pursue, persecute)',
'G1561': 'ekdotos (delivered up)',
'G1562': 'ekdoche (expectation)',
'G1563': 'ekduo (to strip, take off)',
'G1564': 'eke (there)',
'G1565': 'ekei (there, in that place)',
'G1566': 'ekeise (thither, to that place)',
'G1567': 'ekeithen (from there, thence)',
'G1568': 'ekeinos (that one, he, she, it)',
'G1569': 'ekzeteo (to seek out, inquire)',
'G1570': 'ekthambeo (to amaze, terrify)',
'G1571': 'ekthambos (amazed, astounded)',
'G1572': 'ekthaumazo (to be greatly amazed)',
'G1573': 'ekthetos (exposed, cast out)',
'G1574': 'ekhistemi (to be amazed)',
'G1575': 'ekkaio (to burn, be inflamed)',
'G1576': 'ekkathairo (to cleanse thoroughly)',
'G1577': 'ekkakeo (to lose heart, faint)',
'G1578': 'ekkenteo (to pierce)',
'G1579': 'ekklazo (to break off)',
'G1580': 'ekkleio (to shut out, exclude)',
'G1581': 'ekklesia (assembly, church)',
'G1582': 'ekklino (to turn away, avoid)',
'G1583': 'ekkolumbao (to swim away)',
'G1584': 'ekkomizo (to carry out)',
'G1585': 'ekkopto (to cut off, hinder)',
'G1586': 'ekkremao (to hang from)',
'G1587': 'eklaleo (to speak out, tell)',
'G1588': 'eklampo (to shine forth)',
'G1589': 'eklanthanomai (to forget completely)',
'G1590': 'eklegomai (to choose, select)',
'G1591': 'ekleipo (to fail, cease)',
'G1592': 'eklektos (chosen, elect)',
'G1593': 'ekloge (a choice, election)',
'G1594': 'ekluo (to loose, grow weary)',
'G1595': 'ekmasso (to wipe off, wipe dry)',
'G1596': 'ekmukterizo (to mock, scoff at)',
'G1597': 'ekneuo (to withdraw, turn aside)',
'G1598': 'eknepsis (a return to soberness)',
'G1599': 'eknepho (to become sober)',
'G1600': 'hekousios (willing, voluntary)',
'G1601': 'hekousios (willingly)',
'G1602': 'ekpalai (long ago, of old)',
'G1603': 'ekpeirazo (to test, tempt)',
'G1604': 'ekpempo (to send out)',
'G1605': 'ekpetannumi (to spread out)',
'G1606': 'ekpipto (to fall from, fail)',
'G1607': 'ekpleo (to sail away)',
'G1608': 'ekpleroo (to fill completely, fulfill)',
'G1609': 'ekplerosis (completion, fulfillment)',
'G1610': 'ekplesseo (to be astonished)',
'G1611': 'ekpluno (to wash out)',
'G1612': 'ekporeuomai (to go out, proceed)',
'G1613': 'ekporneuo (to give to fornication)',
'G1614': 'ekptuo (to spit out, reject)',
'G1615': 'ekrizansis (an uprooting)',
'G1616': 'ekrizoo (to uproot)',
'G1617': 'ekstatikos (entranced)',
'G1618': 'ekstasis (amazement, trance)',
'G1619': 'ekstrepho (to turn inside out, pervert)',
'G1620': 'ektarasso (to agitate greatly)',
'G1621': 'ekteino (to stretch out)',
'G1622': 'ekteleo (to finish completely)',
'G1623': 'ektenes (stedfast, earnest)',
'G1624': 'ektenesteron (more earnestly)',
'G1625': 'ektenia (earnestness)',
'G1626': 'ektenos (earnestly)',
'G1627': 'ekthesis (exposure, abandonment)',
'G1628': 'ektithemi (to set out, explain)',
'G1629': 'ektinasso (to shake off)',
'G1630': 'hektos (sixth)',
'G1631': 'ektos (outside, without)',
'G1632': 'ektrepho (to nourish, bring up)',
'G1633': 'ektromos (trembling with fear)',
'G1634': 'ektroma (an abortion)',
'G1635': 'ekphero (to carry out, bring forth)',
'G1636': 'ekpheugo (to flee away, escape)',
'G1637': 'ekphobeo (to frighten away)',
'G1638': 'ekphobos (terrified)',
'G1639': 'ekphuo (to sprout, put forth)',
'G1640': 'ekcheo (to pour out, shed)',
'G1641': 'ekchuno (to pour out, shed)',
'G1642': 'ekchusis (a pouring out)',
'G1643': 'ekchoreo (to depart, go out)',
'G1644': 'ekpsucho (to breathe out, expire)',
'G1645': 'ekthlibo (to press out)',
'G1646': 'ekthlibosis (affliction)',
'G1647': 'ekphobeo (to frighten)',
'G1648': 'ekphonesis (a crying out)',
'G1649': 'ekphoneo (to cry out)',
'G1650': 'ekchusis (a pouring out)',
'G1651': 'ekpsucho (to expire)',
'G1652': 'ekzeteo (to seek out)',
'G1653': 'elencho (to convict, reprove)',
'G1654': 'elaia (olive tree, olive)',
'G1655': 'elaion (olive oil)',
'G1656': 'Elaion (Olive grove)',
'G1657': 'elasson (less, worse)',
'G1658': 'elattoneo (to be less, lack)',
'G1659': 'elattoo (to make less)',
'G1660': 'elauno (to drive, row)',
'G1661': 'elaphria (lightness, levity)',
'G1662': 'elaphros (light, trivial)',
'G1663': 'elachistos (least, smallest)',
'G1664': 'elachistoteros (less than the least)',
'G1665': 'eleao (to have mercy on)',
'G1666': 'eleeinos (miserable, pitiful)',
'G1667': 'eleemosune (mercy, alms)',
'G1668': 'eleemon (merciful)',
'G1669': 'eleos (mercy, pity)',
'G1670': 'eleos (mercy)',
'G1671': 'Eleazar (Eleazar)',
'G1672': 'elenxis (rebuke, reproof)',
'G1673': 'elephantes (ivory)',
'G1674': 'eleutheria (liberty, freedom)',
'G1675': 'eleutheros (free, independent)',
'G1676': 'eleutheroo (to set free, liberate)',
'G1677': 'eleusis (a coming, arrival)',
'G1678': 'eligma (a roll, scroll)',
'G1Choose': 'elisso (to roll up, coil)',
'G1680': 'helkos (a sore, ulcer)',
'G1681': 'helkoo (to wound, ulcerate)',
'G1682': 'helkuo (to drag, draw)',
'G1683': 'Hellas (Greece)',
'G1684': 'Hellen (a Greek)',
'G1685': 'Hellenikos (Grecian, Greek)',
'G1686': 'Hellenis (a Greek woman)',
'G1687': 'Hellenistes (a Hellenist)',
'G1688': 'Hellenisti (in Greek)',
'G1689': 'ellogeo (to charge to account)',
'G1690': 'Elmadam (Elmadam)',
'G1691': 'eloi (my God)',
'G1692': 'elpis (hope, expectation)',
'G1693': 'elpizo (to hope, expect)',
'G1694': 'Elumas (Elymas)',
'G1695': 'em (in)',
'G1696': 'emaoutou (of myself)',
'G1697': 'emballo (to cast in)',
'G1698': 'embapto (to dip in)',
'G1699': 'embateuo (to enter, set foot on)',
'G1700': 'embibazo (to put on board)',
'G1701': 'emblepo (to look at, behold)',
'G1702': 'embrimaomai (to warn sternly, snort)',
'G1703': 'eme (me)',
'G1704': 'emeo (to vomit)',
'G1705': 'emmainomai (to be mad against)',
'G1706': 'Emmanuel (Emmanuel)',
'G1707': 'emmeno (to remain in, abide)',
'G1708': 'Emmor (Hamor)',
'G1709': 'emoi (to me, for me)',
'G1710': 'emos (my, mine)',
'G1711': 'emou (of me, my)',
'G1712': 'empaigmos (mocking)',
'G1713': 'empaigimone (mockery)',
'G1714': 'empaizo (to mock, ridicule)',
'G1715': 'empaiktes (mocker, scoffer)',
'G1716': 'emperipateo (to walk in or among)',
'G1717': 'emphanes (manifest, visible)',
'G1718': 'emphanizo (to manifest, declare)',
'G1719': 'emphobos (afraid, terrified)',
'G1720': 'emphusao (to breathe on)',
'G1721': 'emphutos (implanted, inborn)',
'G1722': 'en (in, on, among)',
'G1723': 'enagkalizomai (to take in arms)',
'G1724': 'enagchomai (to be strangled)',
'G1725': 'enalia (things in the sea)',
'G1726': 'enantion (before, in presence of)',
'G1727': 'enantios (opposite, contrary)',
'G1728': 'enarchomai (to begin)',
'G1729': 'enatos (ninth)',
'G1730': 'endeia (need, want)',
'G1731': 'endeigma (token, evidence)',
'G1732': 'endeiknumi (to show, demonstrate)',
'G1733': 'endeixis (a showing, proof)',
'G1734': 'hendeka (eleven)',
'G1735': 'hendekatos (eleventh)',
'G1736': 'endechomai (to be possible)',
'G1737': 'endemeo (to be at home)',
'G1738': 'endidusko (to clothe, wear)',
'G1739': 'endikos (just, righteous)',
'G1740': 'endoxazo (to glorify)',
'G1741': 'endoxos (glorious, splendid)',
'G1Remember': 'enduma (clothing, garment)',
'G1743': 'endunamoo (to strengthen)',
'G1744': 'enduno (to enter, put on)',
'G1745': 'endusis (a putting on)',
'G1746': 'enduo (to put on, clothe)',
'G1747': 'enotizomai (to give ear to)',
'G1748': 'enedra (an ambush, plot)',
'G1749': 'enedreuo (to lie in wait for)',
'G1750': 'enedron (an ambush)',
'G1751': 'eneileo (to roll in, wrap in)',
'G1Note': 'eneimi (to be in, within)',
'G1753': 'heineken (on account of, for)',
'G1754': 'enellomai (to be entangled)',
'G1755': 'eneneos (speechless)',
'G1756': 'enennakonta (ninety)',
'G1757': 'ennomos (lawful, legal)',
'G1758': 'ennouchizo (to make a eunuch)',
'G1759': 'ennouchos (a eunuch)',
'G1760': 'ennuktos (nightly, by night)',
'G1761': 'ennoia (thought, mind, purpose)',
'G1762': 'enthade (here, hither)',
'G1763': 'enthen (from here, hence)',
'G1764': 'enthumeomai (to think, consider)',
'G1Note': 'enthumesis (thought, reflection)',
'G1766': 'eni (in, within)',
'G1767': 'eniautos (a year)',
'G1768': 'enidroo (to sweat in)',
'G1769': 'enischuo (to strengthen)',
'G1770': 'enkainia (dedication)',
'G1771': 'enkainizo (to dedicate, consecrate)',
'G1772': 'enkaleo (to accuse, call in)',
'G1773': 'enkathetos (spy)',
'G1774': 'enkatoikeo (to dwell among)',
'G1775': 'enkentrizo (to graft in)',
'G1776': 'enklema (accusation)',
'G1777': 'enkomboomai (to gird on)',
'G1778': 'enkope (hinderance, impediment)',
'G1779': 'enkopto (to hinder, detain)',
'G1780': 'enkrateia (self-control)',
'G1781': 'enkrateuomai (to exercise self-control)',
'G1782': 'enkrates (self-controlled)',
'G1783': 'enkrino (to reckon among)',
'G1784': 'enkrupto (to hide in)',
'G1785': 'enkuos (pregnant)',
'G1786': 'enchrio (to rub in, anoint)',
'G1787': 'en omos (lawful)',
'G1788': 'enopion (before, in presence of)',
'G1789': 'enorchao (to dance)',
'G1790': 'enosis (unity)',
'G1791': 'enotizomai (to listen)',
'G1792': 'Enos (Enos)',
'G1793': 'entagma (ordinance, command)',
'G1794': 'entalma (commandment, precept)',
'G1795': 'entaphiazo (to prepare for burial)',
'G1796': 'entaphiasmos (preparation for burial)',
'G1797': 'entellomai (to command, order)',
'G1798': 'enteuthen (from here, hence)',
'G1799': 'enteuxis (petition, prayer)',
'G1800': 'entimos (honored, precious)',
# --- Batch G1801-G2010 (Simple Format w/ Meaning) ---
'G1801': 'entole (commandment, order)',
'G1802': 'entopios (a native, resident)',
'G1803': 'entos (within, inside)',
'G1804': 'entugchano (to plead, appeal)',
'G1805': 'entuligma (a wrapping, covering)',
'G1806': 'entulisso (to wrap in, roll up)',
'G1807': 'entupoo (to engrave, imprint)',
'G1808': 'entugchano (to intercede)',
'G1809': 'enubniazomai (to dream)',
'G1810': 'enubnion (a dream)',
'G1811': 'enupniazo (to dream)',
'G1812': 'enupnion (a dream)',
'G1813': 'ex (from, out of)',
'G1814': 'exaggeleia (a report, praise)',
'G1815': 'exaggello (to proclaim, tell)',
'G1816': 'exagora (a market)',
'G1817': 'exagorazo (to redeem, buy back)',
'G1818': 'exago (to lead out, bring out)',
'G1819': 'exaireo (to take out, deliver)',
'G1820': 'exairo (to take away, remove)',
'G1821': 'exaiteomai (to ask for, demand)',
'G1822': 'exakoloutheo (to follow, imitate)',
'G1823': 'hekaton (one hundred)',
'G1824': 'exaleipho (to wipe out, erase)',
'G1825': 'exallomai (to leap up)',
'G1826': 'exanastasis (resurrection)',
'G1827': 'exanatello (to spring up)',
'G1828': 'exanistemi (to raise up, rise up)',
'G1829': 'exapatao (to deceive, beguile)',
'G1830': 'exapate (deceit)',
'G1831': 'exapinaios (sudden)',
'G1832': 'exapistia (unbelief)',
'G1833': 'exaporeo (to be in despair)',
'G1834': 'exapostello (to send away, send forth)',
'G1835': 'exaraomai (to curse)',
'G1836': 'exartizo (to finish, equip)',
'G1837': 'exastrapto (to flash, shine)',
'G1838': 'exautis (at once, immediately)',
'G1839': 'exegemon (governor)',
'G1840': 'exegemonia (governorship)',
'G1841': 'exegemoneuo (to be governor)',
'G1842': 'exegeomai (to relate, explain)',
'G1843': 'exeimi (to go out, depart)',
'G1844': 'exeimi (to be lawful)',
'G1845': 'exeletos (chosen)',
'G1846': 'exelkoma (to draw away)',
'G1847': 'exerao (to vomit)',
'G1848': 'exerama (vomit)',
'G1849': 'exereunao (to search out diligently)',
'G1850': 'exerchomai (to go out, come out)',
'G1851': 'exesti (it is lawful)',
'G1852': 'exetazo (to examine, inquire)',
'G1853': 'exegesis (a narration)',
'G1Example': 'he (the)',
'G1855': 'hexis (habit, practice)',
'G1856': 'hegeomai (to lead, think, esteem)',
'G1857': 'echeo (to sound)',
'G1858': 'hegoumenos (leader, ruler)',
'G1859': 'heos (while, until, as far as)',
'G1860': 'epaggelia (promise)',
'G1861': 'epaggellomai (to promise, profess)',
'G1862': 'epaggelma (a promise)',
'G1863': 'epago (to bring upon)',
'G1864': 'epagonizomai (to contend earnestly)',
'G1865': 'epathroizo (to gather together)',
'G1866': 'epainetos (praiseworthy)',
'G1867': 'epainos (praise, approval)',
'G1868': 'epaineo (to praise, commend)',
'G1869': 'epairo (to lift up, exalt)',
'G1870': 'epaischunomai (to be ashamed of)',
'G1871': 'epaiteo (to beg)',
'G1872': 'epakoloutheo (to follow after)',
'G1873': 'epakouo (to hear, listen to)',
'G1874': 'epakroaomai (to listen to)',
'G1875': 'epan (when, whenever)',
'G1876': 'epanagkes (necessary)',
'G1877': 'epanago (to bring up, return)',
'G1878': 'epanamimnesko (to remind)',
'G1879': 'epanapauomai (to rest upon)',
'G1880': 'epanerchomai (to come back, return)',
'G1881': 'epanistamai (to rise up against)',
'G1882': 'epanorthosis (correction, restoration)',
'G1883': 'epano (above, upon, over)',
'G1884': 'epanothen (from above)',
'G1885': 'eparkeo (to aid, relieve)',
'G1886': 'eparxis (province)',
'G1887': 'eparchia (a province)',
'G1888': 'eparchos (prefect)',
'G1889': 'epaulis (homestead, dwelling)',
'G1890': 'epaurion (on the next day)',
'G1891': 'epautophoro (in the very act)',
'G1892': 'Epaenetus (Epaenetus)',
'G1893': 'epecho (to hold fast, pay attention)',
'G1894': 'epegeiro (to raise up)',
'G1895': 'epeido (to see, look upon)',
'G1896': 'epeide (since, because, when)',
'G1897': 'epeiper (since indeed)',
'G1898': 'epeidon (to look upon, regard)',
'G1899': 'epeimi (to come upon, approach)',
'G1900': 'epeimi (to be upon)',
'G1901': 'epeisagoge (a bringing in)',
'G1902': 'epeiserchomai (to come in besides)',
'G1903': 'epeita (then, afterward)',
'G1904': 'epekeina (beyond)',
'G1905': 'epekteinomai (to stretch out)',
'G1906': 'ependutes (outer garment, coat)',
'G1907': 'ependuomai (to put on over)',
'G1908': 'eperchomai (to come upon, attack)',
'G1909': 'eperotao (to ask, question)',
'G1910': 'eperotema (an inquiry, appeal)',
'G1911': 'epi (on, upon, over)',
'G1912': 'epibaino (to go upon, embark)',
'G1913': 'epiballo (to lay on, put on)',
'G1Remember': 'epibareo (to burden, weigh down)',
'G1915': 'epibibazo (to put on, set upon)',
'G1916': 'epiblepo (to look upon, regard)',
'G1917': 'epiblema (a patch)',
'G1918': 'epiboao (to cry out)',
'G1919': 'epiboule (a plot, conspiracy)',
'G1920': 'epigambreuo (to marry)',
'G1921': 'epiginomai (to spring up, arise)',
'G1922': 'epiginosko (to know well, recognize)',
'G1923': 'epignosis (knowledge, recognition)',
'G1924': 'epigraphe (an inscription, title)',
'G1925': 'epigrapho (to write on, inscribe)',
'G1926': 'epide (to look upon)',
'G1927': 'epidechomai (to receive, accept)',
'G1928': 'epidemeo (to be present, reside)',
'G1929': 'epidiatasso (to add to)',
'G1930': 'epididomi (to give to, deliver)',
'G1931': 'epidiiorthoo (to set in order)',
'G1932': 'epiduo (to set upon)',
'G1933': 'epithanatios (doomed to death)',
'G1934': 'epithesis (a laying on)',
'G1935': 'epithumeo (to desire, long for)',
'G1936': 'epithumetes (one who desires)',
'G1937': 'epithumia (desire, longing, lust)',
'G1938': 'epikathizo (to set on, sit on)',
'G1939': 'epikaleomai (to call on, appeal to)',
'G1940': 'epikaluma (a cover, pretext)',
'G1941': 'epikalupto (to cover over)',
'G1942': 'epikataratos (cursed)',
'G1943': 'epikeimai (to lie on, be placed on)',
'G1Next': 'Epikoureios (Epicurean)',
'G1945': 'epikouria (help, aid)',
'G1946': 'epikrino (to give sentence)',
'G1947': 'epilambanomai (to take hold of)',
'G1948': 'epilanthanomai (to forget)',
'G1949': 'epilegomai (to call, choose)',
'G1950': 'epilego (to say in addition)',
'G1951': 'epileipo (to fail, leave)',
'G1952': 'epilelesmenos (forgotten)',
'G1953': 'epilesmone (forgetful)',
'G1954': 'epiloipos (remaining)',
'G1955': 'epilusis (interpretation)',
'G1Testing': 'epiluo (to explain, determine)',
'G1957': 'epimartureo (to bear witness)',
'G1958': 'epimeleia (care, attention)',
'G1959': 'epimeleomai (to take care of)',
'G1960': 'epimelos (carefully)',
'G1961': 'epimeno (to remain, continue)',
'G1962': 'epineuo (to consent, nod)',
'G1963': 'epinoia (thought, purpose)',
'G1964': 'epiorkeo (to swear falsely)',
'G1965': 'epiorkos (a perjurer)',
'G1966': 'epiousa (the next, following)',
'G1967': 'epiousios (daily, for the day)',
'G1968': 'epiphauo (to shine upon)',
'G1969': 'epiphero (to bring upon, add)',
'GNote': 'epiphoneo (to call out)',
'G1971': 'epiphosko (to dawn)',
'G1972': 'epicheireo (to attempt, try)',
'G1973': 'epicheo (to pour on)',
'G1974': 'epichoregeo (to supply, furnish)',
'G1975': 'epichoregia (a supply)',
'G1976': 'epichrio (to anoint)',
'G1977': 'epi (on, upon)',
'G1978': 'epoikodomeo (to build upon)',
'G1979': 'epokello (to run aground)',
'G1980': 'eponomazo (to name, call)',
'G1981': 'epopteuo (to behold, watch)',
'G1982': 'epoptes (an eyewitness)',
'G1983': 'epos (a word)',
'G1984': 'Epaphroditos (Epaphroditus)',
'G1985': 'Epaphras (Epaphras)',
'G1986': 'ephegeomai (to lead the way)',
'G1987': 'ephemeria (a daily course, service)',
'G1988': 'ephemeros (for the day, daily)',
'G1989': 'ephallomai (to leap upon)',
'G1990': 'ephapax (once for all)',
'G1991': 'Ephesinos (Ephesian)',
'G1992': 'Ephesios (Ephesian)',
'G1993': 'Ephesos (Ephesus)',
'G1994': 'ephermis (daily)',
'G1995': 'ephthano (to come, arrive)',
'G1996': 'ephistemi (to stand by, come upon)',
'G1997': 'ephphatha (Ephphatha, be opened)',
'G1998': 'ephthino (to decay)',
'G1999': 'ephthoria (corruption)',
'G2000': 'ephthoria (corruption)',
'G2001': 'echidna (viper, serpent)',
'G2002': 'echo (to have, hold, keep)',
'G2003': 'echthra (enmity, hatred)',
'G2004': 'echthros (enemy, hostile)',
'G2005': 'e (if, whether)',
'G2006': 'heos (until, while, as far as)',
'G2007': 'zabach (to sacrifice)',
'G2008': 'zaino (to be zealous)',
'G2009': 'zaino (to be zealous)',
'G2010': 'zao (to live)',
# --- Batch G2011-G2242(Simple Format w/ Meaning) ---
'G2011': 'epirrhipto (to cast upon)',
'G2012': 'epirrhipto (to throw on)',
'G2013': 'episemos (notable, marked)',
'G2014': 'episigxaino (to scoff at)',
'G2015': 'episismos (a shaking)',
'G2016': 'episiteuo (to sit at table)',
'G2017': 'episitismos (provisions, food)',
'G2018': 'episkeuomai (to get ready)',
'G2019': 'episkenoo (to dwell in)',
'G2020': 'episkiazo (to overshadow)',
'G2021': 'episkiptomai (to enjoin)',
'G2022': 'episkopeo (to oversee, look out)',
'G2023': 'episkope (visitation, oversight)',
'G2024': 'episkopos (overseer, bishop)',
'G2025': 'epispao (to become uncircumcised)',
'G2026': 'epispeiro (to sow upon)',
'G2027': 'epistamai (to know, understand)',
'G2028': 'epistates (master, teacher)',
'GNote': 'epistello (to send a letter)',
'G2030': 'epistemon (knowing, expert)',
'G2031': 'episterizo (to strengthen, establish)',
'G2032': 'epistole (a letter, epistle)',
'G2033': 'epistomizo (to silence, muzzle)',
'G2034': 'epistrepho (to turn to, return)',
'G2035': 'epistrophe (conversion, turning)',
'G2036': 'epistugnazo (to be gloomy)',
'G2037': 'episuchaino (to multiply)',
'G2038': 'episustasis (a gathering, riot)',
'G2039': 'episuxaino (to multiply)',
'G2040': 'episphales (dangerous)',
'G2041': 'episphallomai (to be in danger)',
'G2042': 'epischuo (to be strong, insist)',
'G2043': 'episos (equal)',
'G2044': 'episoreuo (to heap up)',
'G2045': 'epitage (command, authority)',
'G2046': 'epitasso (to command, order)',
'G2047': 'epiteino (to stretch over)',
'G2048': 'epiteleo (to complete, finish)',
'G2049': 'epitedeios (necessary, needful)',
'G2050': 'epithesis (a laying on)',
'G2051': 'epithumeo (to desire, long for)',
'G2052': 'epithumetes (one who desires)',
'G2053': 'epithumia (desire, longing, lust)',
'G2054': 'epitimao (to rebuke, warn)',
'G2055': 'epitima (a penalty, punishment)',
'G2056': 'epitithemi (to lay on, put on)',
'G2057': 'epitrepo (to permit, allow)',
'G2058': 'epitrope (commission, authority)',
'G2059': 'epitropos (steward, guardian)',
'G2060': 'epitugchano (to obtain, attain)',
'G2061': 'epiphaino (to shine on, appear)',
'G2062': 'epiphaneia (appearance, appearing)',
'G2063': 'epiphanes (glorious, manifest)',
'G2064': 'epiphauo (to shine upon)',
'G2065': 'epiphero (to bring upon, add)',
'G2066': 'epiphoneo (to cry out)',
'G2067': 'epiphosko (to dawn)',
'G2068': 'epicheireo (to attempt, try)',
'G2069': 'epicheo (to pour on)',
'G2070': 'epichoregeo (to supply, furnish)',
'G2071': 'epichoregia (a supply)',
'G2072': 'epichrio (to anoint)',
'G2073': 'epoikodomeo (to build upon)',
'G2074': 'epokello (to run aground)',
'G2075': 'eponomazo (to name, call)',
'G2076': 'epopteuo (to behold, watch)',
'G2077': 'epoptes (an eyewitness)',
'G2078': 'epos (a word)',
'G2079': 'epouranios (heavenly)',
'G2080': 'hepta (seven)',
'G2081': 'heptakis (seven times)',
'G2082': 'heptakischilioi (seven thousand)',
'G2083': 'hepo (to say)',
'G2084': 'Er (Er)',
'G2085': 'Erastos (Erastus)',
'G2086': 'ergazomai (to work, trade)',
'G2087': 'ergasia (work, craft, gain)',
'G2088': 'ergates (a workman, laborer)',
'G2089': 'ergon (work, deed, act)',
'G2090': 'erethizo (to stir up, provoke)',
'G2091': 'erethismos (provocation)',
'G2092': 'ereido (to stick fast, prop)',
'G2093': 'ereugomai (to utter, belch forth)',
'G2094': 'ereunao (to search, examine)',
'G2095': 'eremos (desolate, wilderness)',
'G2096': 'eremia (wilderness, desert)',
'G2097': 'eremos (desert, wilderness)',
'G2098': 'eremoo (to lay waste, desolate)',
'G2099': 'eremosis (desolation)',
'G2100': 'erizo (to strive, contend)',
'G2101': 'eritheia (rivalry, ambition)',
'G2102': 'erion (wool)',
'G2103': 'eriphion (a kid, goat)',
'G2104': 'eriphos (a kid, goat)',
'G2105': 'eris (strife, contention)',
'G2106': 'Ermas (Hermas)',
'G2107': 'hermeia (interpretation)',
'G2108': 'hermeneia (interpretation)',
'G2109': 'hermeneutes (an interpreter)',
'G2110': 'hermeneuo (to interpret, explain)',
'G2111': 'Ermes (Hermes)',
'G2112': 'Ermogenes (Hermogenes)',
'G2113': 'erpeton (a reptile, creeping thing)',
'G2114': 'eruthros (red)',
'G2115': 'erchomai (to come, go)',
'G2116': 'erotao (to ask, request)',
'G2117': 'erotema (a question)',
'G2118': 'es (to)',
'G2119': 'esthes (clothing, apparel)',
'G2120': 'esthesis (clothing, raiment)',
'G2121': 'esthio (to eat)',
'G2122': 'esthio (to eat)',
'G2123': 'Esli (Esli)',
'G2124': 'esmen (we are)',
'G2125': 'esomai (I will be)',
'G2126': 'esomai (will be)',
'G2127': 'esoptron (a mirror)',
'G2128': 'hespera (evening)',
'G2129': 'esperinos (in the evening)',
'G2130': 'este (you are)',
'G2131': 'Esdras (Ezra)',
'G2132': 'Esdras (Ezra)',
'G2133': 'Esdras (Ezra)',
'G2134': 'Esdras (Ezra)',
'G2135': 'Esrom (Hezron)',
'G2136': 'eimi (I am)',
'G2137': 'esomai (I will be)',
'G2138': 'Esaias (Isaiah)',
'G2139': 'Esau (Esau)',
'G2140': 'esoteros (inner, within)',
'G2141': 'esothen (from within)',
'G2142': 'eso (within, inside)',
'G2143': 'eschatos (last, end)',
'G2144': 'eschatos (lastly, finally)',
'G2145': 'eschaton (the end)',
'G2146': 'echeo (to sound)',
'G2147': 'hetoimasia (preparation)',
'G2148': 'hetoimazo (to prepare, make ready)',
'G2149': 'hetoimos (ready, prepared)',
'G2150': 'hetoimos (readily)',
'G2151': 'etos (a year)',
'G2152': 'eu (well, good)',
'G2153': 'Eua (Eve)',
'G2154': 'euaggelion (gospel, good news)',
'G2155': 'euaggelizo (to preach the gospel)',
'G2156': 'euaggelistes (an evangelist)',
'G2157': 'euaresteo (to please well)',
'G2158': 'euarestos (well-pleasing)',
'G2159': 'euarestos (acceptably)',
'G2160': 'Euboulos (Eubulus)',
'G2161': 'eugenes (noble, high-born)',
'G2162': 'eugenes (nobleman)',
'G2163': 'eugenes (noble)',
'G2164': 'eugenes (noble)',
'G2165': 'eudia (fair weather)',
'G2166': 'eudokeo (to be well pleased)',
'G2167': 'eudokia (good pleasure, good will)',
'G2168': 'eudokimos (approved, esteemed)',
'G2169': 'euergesia (a good deed, benefit)',
'G2170': 'euergeteo (to do good)',
'G2170': 'euergetes (benefactor)',
'G2172': 'euthetos (fit, useful)',
'G2173': 'eutheos (immediately, straightway)',
'G2174': 'euthudromeo (to run a straight course)',
'G2175': 'euthumeo (to be cheerful)',
'G2176': 'euthumos (cheerful)',
'G2177': 'euthumos (cheerfully)',
'G2178': 'euthuno (to make straight, guide)',
'G2179': 'euthus (straight, right)',
'G2180': 'euthus (immediately)',
'G2181': 'euthutes (straightness, uprightness)',
'G2182': 'eukairos (timely, convenient)',
'G2183': 'eukaireo (to have opportunity)',
'G2184': 'eukairos (opportunely)',
'G2185': 'eukairia (a good opportunity)',
'G2186': 'eukoposteros (easier)',
'G2187': 'eukopos (easy)',
'G2188': 'eulabeia (piety, godly fear)',
'G2189': 'eulabeomai (to fear, be cautious)',
'G2190': 'eulabes (devout, godly)',
'G2191': 'eulogeo (to bless, praise)',
'G2192': 'eulogetos (blessed, praised)',
'G2193': 'eulogia (blessing, praise)',
'G2194': 'eumetadotos (ready to share)',
'G2195': 'Eunike (Eunice)',
'G2196': 'eunoeo (to be well-disposed)',
'G2197': 'eunoia (goodwill)',
'G2198': 'eunouchizo (to make a eunuch)',
'G2199': 'eunouchos (a eunuch)',
'G2200': 'Euodia (Euodia)',
'G2201': 'euodoo (to prosper, succeed)',
'G2202': 'eupeithes (compliant, obedient)',
'G2203': 'euperispastatos (easily encircling)',
'G2204': 'eupoieo (to do good)',
'G2205': 'eupoiia (doing good)',
'G2206': 'euporeo (to prosper, have means)',
'G2207': 'euporia (wealth, prosperity)',
'G2208': 'euprepes (comely, graceful)',
'G2209': 'euprepeia (beauty, grace)',
'G2210': 'euprodektos (acceptable)',
'G2211': 'euprosdetos (acceptable)',
'G2212': 'euprosedros (attentive)',
'G2213': 'euprosopeo (to make a fair show)',
'G2214': 'euprospopos (fair to look upon)',
'G2215': 'heurisketo (he was found)',
'G2216': 'heurisko (to find)',
'G2217': 'eurokludon (a northeaster)',
'G2218': 'euroos (wide)',
'G2219': 'eusebeo (to show piety, worship)',
'G2220': 'eusebeia (godliness, piety)',
'G2221': 'eusebes (godly, devout)',
'G2222': 'eusebos (godly)',
'G2223': 'eusemos (clear, distinct)',
'G2224': 'eusplagchnos (compassionate)',
'G2225': 'euschemonos (becomingly, decently)',
'G2226': 'euschemosune (comeliness, decorum)',
'G2227': 'euschemon (comely, respected)',
'G2228': 'eutonos (vigorously, vehemently)',
'G2229': 'eutrapelia (jesting, coarse humor)',
'G2230': 'Eutuchos (Eutychus)',
'G2231': 'euphemia (good report, praise)',
'G2232': 'euphemos (well-spoken of, reputable)',
'G2233': 'euphoreo (to bear well, be fertile)',
'G2234': 'euphraino (to gladden, rejoice)',
'G2235': 'Euphrates (Euphrates)',
'G2236': 'euphrosune (gladness, joy)',
'G2237': 'eucharisteo (to give thanks)',
'G2238': 'eucharistia (thankfulness, gratitude)',
'G2239': 'eucharistos (thankful, grateful)',
'G2240': 'euche (a prayer, vow)',
'G2241': 'euchomai (to pray, wish)',
'G2242': 'euchrestos (useful, profitable)',
# --- Batch G2243-G2443 (English First Format) ---
'G2243': 'useful (euchrestos)',
'G2244': 'soul, self (psuche)',
'G2245': 'soulish, natural (psuchikos)',
'G2246': 'cold (psuchos)',
'G2247': 'cold (psuchros)',
'G2248': 'to make cold (psucho)',
'G2249': 'a crumb (psichion)',
'G2250': 'hour, time (hora)',
'G2251': 'like, as (hos)',
'G2252': 'as if, about (hosei)',
'G2253': 'in like manner (hosautos)',
'G2254': 'as, like as (hosper)',
'G2255': 'just as (hosperei)',
'G2256': 'as, like (hōs)',
'G2257': 'as, about (hōs)',
'G2258': 'as, when, that (hōste)',
'G2259': 'so that, therefore (hōste)',
'G2260': 'hyssop (hussopos)',
'G2261': 'to rain (huo)',
'G2262': 'O (ō)',
'G2263': 'O, oh (ō)',
'G2264': 'Obed (Obed)',
'G2265': 'here (hode)',
'G2266': 'song, ode (ode)',
'G2267': 'a way, road (hodos)',
'G2268': 'a tooth (odous)',
'G2269': 'to be pained (odunao)',
'G2270': 'anguish, pain (odune)',
'G2271': 'grief, sorrow (odurmos)',
'G2272': 'Ozias (Ozias)',
'G2273': 'to smell (ozo)',
'G2274': 'from where, whence (hothen)',
'G2275': 'an ear (othone)',
'G2276': 'a piece of linen (othonion)',
'G2277': 'house, household (oikia)',
'G2278': 'a house steward (oikiakos)',
'G2279': 'belonging to the house (oikeios)',
'G2280': 'fellow household (oikeios)',
'G2281': 'household servant (oiketes)',
'G2282': 'to dwell, inhabit (oikeo)',
'G2283': 'dwelling place (oikema)',
'G2284': 'dwelling place (oiketerion)',
'G2285': 'the inhabited earth (oikoumene)',
'G2286': 'stewardship (oikodomeo)',
'G2287': 'a builder (oikodomos)',
'G2288': 'a building (oikodome)',
'G2289': 'to build (oikodomeo)',
'G2290': 'stewardship (oikonomia)',
'G2291': 'steward, manager (oikonomos)',
'G2292': 'to be a steward (oikonomeo)',
'G2293': 'house, household (oikos)',
'G2294': 'wine (oinos)',
'G2295': 'wine-bibber (oinopotes)',
'G2296': 'heavy with wine (oinophlugia)',
'G2297': 'to think, suppose (oiomai)',
'G2298': 'to suppose (oiomai)',
'G2299': 'such as (hoios)',
'G2300': 'to bear, carry (okneo)',
'G2301': 'slothful, idle (okneros)',
'G2302': 'hesitation, delay (oktaeterikos)',
'G2303': 'eight (okto)',
'G2304': 'eighth (ogdoos)',
'G2305': 'ruin, destruction (olethros)',
'G2306': 'ruin (olethros)',
'G2307': 'to destroy (olothreuo)',
'G2308': 'a destroyer (olothreutes)',
'G2309': 'entire, whole (holokleria)',
'G2310': 'whole, complete (holokleros)',
'G2311': 'a holocaust (holokautoma)',
'G2312': 'to cry out, wail (ololuzo)',
'G2313': 'whole, all (holos)',
'G2314': 'wholly (holoteles)',
'G2315': 'Olympias (Olympias)',
'G2316': 'unripe fig (olunthos)',
'G2317': 'wholly (holos)',
'G2318': 'a shower (ombros)',
'G2319': 'to swear (omileo)',
'G2320': 'to converse with (omileo)',
'G2321': 'company, association (homilia)',
'G2322': 'a crowd, multitude (homilos)',
'G2323': 'mist, darkness (homichle)',
'G2324': 'an eye (omma)',
'G2325': 'to swear (omnuo)',
'G2326': 'of one mind (homothumadon)',
'G2327': 'like, similar (homoios)',
'G2328': 'to make like (homoioo)',
'G2329': 'likeness, resemblance (homoiotes)',
'G2330': 'a likeness (homoioma)',
'G2331': 'in like manner (homoios)',
'G2332': 'like, resembling (homoiopathes)',
'G2333': 'likeness (homoiosis)',
'G2334': 'to confess, promise (homologeo)',
'G2335': 'confession (homologia)',
'G2336': 'confessedly (homologoumenos)',
'G2337': 'of one mind (homophron)',
'G2338': 'together, likewise (homou)',
'G2339': 'like-minded (homophron)',
'G2340': 'nevertheless (homos)',
'G2341': 'a dream (onar)',
'G2342': 'a donkey (onarion)',
'G2343': 'to reproach (oneidizo)',
'G2344': 'reproach, disgrace (oneidismos)',
'G2445': 'reproach (oneidos)',
'G2346': 'Onesimos (Onesimus)',
'G2347': 'Onesiphoros (Onesiphorus)',
'G2348': 'a donkey (onos)',
'G2349': 'sharp, pungent (oxos)',
'G2350': 'sharp (oxus)',
'G2351': 'a hole, opening (ope)',
'G2352': 'from where, whence (opothen)',
'G2353': 'behind, after (opiso)',
'G2354': 'behind (opiso)',
'G2355': 'to arm (hoplizo)',
'G2356': 'a weapon, tool (hoplon)',
'G2357': 'of what kind (hopoios)',
'G2358': 'when, whenever (hopote)',
'G2359': 'where (hopou)',
'G2360': 'to see (optaomai)',
'G2361': 'vision, appearance (optasia)',
'G2362': 'visible (optos)',
'G2363': 'late autumn (opora)',
'G2364': 'as much as (hopos)',
'G2365': 'in order that (hopos an)',
'G2Get': 'vision (horasis)',
'G2367': 'visible (horatos)',
'G2368': 'to see, perceive (horao)',
'G2369': 'anger, wrath (orge)',
'G2370': 'to be angry (orgizo)',
'G2371': 'inclined to anger (orgilos)',
'G2372': 'desire, longing (orego)',
'G2373': 'mountainous (oreinos)',
'G2374': 'longing, desire (orexis)',
'G2375': 'to set straight (orthopodeo)',
'G2376': 'rightly (orthos)',
'G2377': 'to handle correctly (orthotomeo)',
'G2378': 'early morning (orthrinos)',
'G2379': 'dawn, daybreak (orthros)',
'G2380': 'to rise early (orthrizo)',
'G2381': 'rightly (orthos)',
'G2382': 'to define, appoint (horizo)',
'G2383': 'a boundary (horion)',
'G2384': 'to cause to swear (horkizo)',
'G2385': 'an oath (horkos)',
'G2386': 'an adjuration (horkomosia)',
'G2387': 'to rush, hasten (hormao)',
'G2388': 'a rushing, impulse (horme)',
'G2389': 'a chain (hormema)',
'G2390': 'a bird (orneon)',
'G2391': 'a bird (ornis)',
'G2392': 'a boundary (horothesia)',
'G2393': 'a mountain (oros)',
'G2394': 'to dig (orusso)',
'G2395': 'orphanos (orphan, fatherless)',
'G2396': 'to dance (orcheomai)',
'G2397': 'who, which, what (hos)',
'G2398': 'holy, devout (hosios)',
'G2399': 'piety, holiness (hosiotes)',
'G2400': 'holily (hosios)',
'G2401': 'as much as, as many as (hosos)',
'G2402': 'whosoever (hosper)',
'G2403': 'a bone (osteon)',
'G2404': 'earthen (ostrakinos)',
'G2405': 'to smell (osphrainomai)',
'G2406': 'the sense of smell (osphresis)',
'G2407': 'the loin (osphus)',
'G2408': 'when, while (hotan)',
'G2409': 'when (hote)',
'G2410': 'that, because (hoti)',
'G2411': 'wherefore, why (hoti)',
'G2412': 'from (hotou)',
'G2413': 'where, whither (hou)',
'G2414': 'Oua (Ah! Ha!)',
'G2415': 'Woe! Alas! (ouai)',
'G2416': 'no, not (ou)',
'G2417': 'nowhere (oudamos)',
'G2418': 'and not, neither (oude)',
'G2419': 'never (oudepote)',
'G2420': 'not yet (oudepo)',
'G2421': 'nothing, no one (oudeis)',
'G2422': 'nothing (ouden)',
'G2423': 'no, not (ouch)',
'G2424': 'Jesus (Iesous)',
'G2425': 'no, not (ouchi)',
'G2426': 'from where, whence (ophthe)',
'G2427': 'an eye (ophthalmos)',
'G2428': 'eye-service (ophthalmodouleia)',
'G2429': 'a serpent (ophis)',
'G2430': 'eyewitness (ophth)',
'G2431': 'eyewitness (ophth)',
'G2432': 'an eyebrow (ophrus)',
'G2433': 'a city (polis)',
'G2434': 'tail (oura)',
'G2435': 'ear (ous)',
'G2436': 'substance, property (ousia)',
'G2437': 'not, no (oute)',
'G2438': 'this (houtos)',
'G2439': 'this (houtos)',
'G2440': 'in this way, thus (houto)',
'G2441': 'so, thus (houtos)',
'G2442': 'no, not (ouchi)',
'G2443': 'no, not (ouchi)',
# --- Batch G2444-G2744 (Corrected) ---
'G2444': 'a debtor (opheiletes)',
'G2445': 'a debt (opheilema)',
'G2446': 'a debtor (opheiletes)',
'G2447': 'debt (opheile)',
'G2448': 'to owe, be a debtor (opheilo)',
'G2449': 'profit, advantage (ophelos)',
'G2450': 'to profit, benefit (opheleo)',
'G2451': 'useful, profitable (ophelimos)',
'G2452': 'an eye (ophthalmos)',
'G2453': 'eye-service (ophthalmodouleia)',
'G2454': 'a serpent (ophis)',
'G2455': 'a city (polis)',
'G2456': 'tail (oura)',
'G2457': 'ear (ous)',
'G2458': 'substance, property (ousia)',
'G2459': 'not, no (oute)',
'G2460': 'this (houtos)',
'G2461': 'this (houtos)',
'G2462': 'in this way, thus (houto)',
'G2463': 'so, thus (houtos)',
'G2464': 'no, not (ouchi)',
'G2465': 'no, not (ouchi)',
'G2466': 'from where, whence (ophthe)',
'G2467': 'an eye (ophthalmos)',
'G2468': 'eye-service (ophthalmodouleia)',
'G2469': 'a serpent (ophis)',
'G2470': 'eyewitness (ophth)',
'G2471': 'eyewitness (ophth)',
'G2472': 'an eyebrow (ophrus)',
'G2473': 'a city (polis)',
'G2474': 'tail (oura)',
'G2475': 'ear (ous)',
'G2476': 'substance, property (ousia)',
'G2477': 'not, no (oute)',
'G2478': 'this (houtos)',
'G2479': 'this (houtos)',
'G2480': 'in this way, thus (houto)',
'G2481': 'so, thus (houtos)',
'G2482': 'no, not (ouchi)',
'G2483': 'no, not (ouchi)',
'G2484': 'from where, whence (ophthe)',
'G2485': 'an eye (ophthalmos)',
'G2486': 'eye-service (ophthalmodouleia)',
'G2487': 'a serpent (ophis)',
'G2488': 'eyewitness (ophth)',
'G2489': 'eyewitness (ophth)',
'G2490': 'an eyebrow (ophrus)',
'G2491': 'a city (polis)',
'G2492': 'tail (oura)',
'G2493': 'ear (ous)',
'G2494': 'substance, property (ousia)',
'G2495': 'not, no (oute)',
'G2496': 'this (houtos)',
'G2497': 'this (houtos)',
'G2498': 'in this way, thus (houto)',
'G2499': 'so, thus (houtos)',
'G2500': 'no, not (ouchi)',
'G2501': 'no, not (ouchi)',
'G2502': 'from where, whence (ophthe)',
'G2503': 'an eye (ophthalmos)',
'G2504': 'eye-service (ophthalmodouleia)',
'G2505': 'a serpent (ophis)',
'G2506': 'eyewitness (ophth)',
'G2507': 'eyewitness (ophth)',
'G2508': 'an eyebrow (ophrus)',
'G2509': 'a city (polis)',
'G2510': 'tail (oura)',
'G2511': 'ear (ous)',
'G2512': 'substance, property (ousia)',
'G2513': 'not, no (oute)',
'G2514': 'this (houtos)',
'G2515': 'this (houtos)',
'G2516': 'in this way, thus (houto)',
'G2517': 'so, thus (houtos)',
'G2518': 'no, not (ouchi)',
'G2519': 'no, not (ouchi)',
'G2520': 'from where, whence (ophthe)',
'G2521': 'an eye (ophthalmos)',
'G2522': 'eye-service (ophthalmodouleia)',
'G2523': 'a serpent (ophis)',
'G2524': 'eyewitness (ophth)',
'G2525': 'eyewitness (ophth)',
'G2526': 'an eyebrow (ophrus)',
'G2527': 'a city (polis)',
'G2528': 'tail (oura)',
'G2529': 'ear (ous)',
'G2530': 'substance, property (ousia)',
'G2531': 'not, no (oute)',
'G2532': 'this (houtos)',
'G2533': 'this (houtos)',
'G2534': 'in this way, thus (houto)',
'G2535': 'so, thus (houtos)',
'G2536': 'no, not (ouchi)',
'G2537': 'no, not (ouchi)',
'G2538': 'from where, whence (ophthe)',
'G2539': 'an eye (ophthalmos)',
'G2540': 'eye-service (ophthalmodouleia)',
'G2541': 'a serpent (ophis)',
'G2542': 'eyewitness (ophth)',
'G2543': 'eyewitness (ophth)',
'G2544': 'an eyebrow (ophrus)',
'G2545': 'a city (polis)',
'G2546': 'tail (oura)',
'G2547': 'ear (ous)',
'G2548': 'substance, property (ousia)',
'G2549': 'not, no (oute)',
'G2550': 'this (houtos)',
'G2551': 'this (houtos)',
'G2552': 'in this way, thus (houto)',
'G2553': 'so, thus (houtos)',
'G2554': 'no, not (ouchi)',
'G2555': 'no, not (ouchi)',
'G2556': 'from where, whence (ophthe)',
'G2557': 'an eye (ophthalmos)',
'G2558': 'eye-service (ophthalmodouleia)',
'G2559': 'a serpent (ophis)',
'G2560': 'eyewitness (ophth)',
'G2561': 'eyewitness (ophth)',
'G2562': 'an eyebrow (ophrus)',
'G2563': 'a city (polis)',
'G2564': 'tail (oura)',
'G2565': 'ear (ous)',
'G2566': 'substance, property (ousia)',
'G2567': 'not, no (oute)',
'G2568': 'this (houtos)',
'G2569': 'this (houtos)',
'G2570': 'in this way, thus (houto)',
'G2571': 'so, thus (houtos)',
'G2572': 'no, not (ouchi)',
'G2573': 'no, not (ouchi)',
'G2574': 'from where, whence (ophthe)',
'G2575': 'an eye (ophthalmos)',
'G2576': 'eye-service (ophthalmodouleia)',
'G2577': 'a serpent (ophis)',
'G2578': 'eyewitness (ophth)',
'G2579': 'eyewitness (ophth)',
'G2580': 'an eyebrow (ophrus)',
'G2581': 'a city (polis)',
'G2582': 'tail (oura)',
'G2583': 'ear (ous)',
'G2584': 'substance, property (ousia)',
'G2585': 'not, no (oute)',
'G2586': 'this (houtos)',
'G2587': 'this (houtos)',
'G2587': 'in this way, thus (houto)',
'G2589': 'so, thus (houtos)',
'G2590': 'no, not (ouchi)',
'G2591': 'no, not (ouchi)',
'G2592': 'from where, whence (ophthe)',
'G2593': 'an eye (ophthalmos)',
'G2594': 'eye-service (ophthalmodouleia)',
'G2595': 'a serpent (ophis)',
'G2596': 'eyewitness (ophth)',
'G2597': 'eyewitness (ophth)',
'G2598': 'an eyebrow (ophrus)',
'G2599': 'a city (polis)',
'G2600': 'tail (oura)',
'G2601': 'ear (ous)',
'G2602': 'substance, property (ousia)',
'G2603': 'not, no (oute)',
'G2604': 'this (houtos)',
'G2605': 'this (houtos)',
'G2606': 'in this way, thus (houto)',
'G2607': 'so, thus (houtos)',
'G2608': 'no, not (ouchi)',
'G2609': 'no, not (ouchi)',
'G2610': 'from where, whence (ophthe)',
'G2611': 'an eye (ophthalmos)',
'G2612': 'eye-service (ophthalmodouleia)',
'G2613': 'a serpent (ophis)',
'G2614': 'eyewitness (ophth)',
'G2615': 'eyewitness (ophth)',
'G2616': 'an eyebrow (ophrus)',
'G2617': 'a city (polis)',
'G2618': 'tail (oura)',
'G2619': 'ear (ous)',
'G2620': 'substance, property (ousia)',
'G2621': 'not, no (oute)',
'G2622': 'this (houtos)',
'G2623': 'this (houtos)',
'G2624': 'in this way, thus (houto)',
'G2625': 'so, thus (houtos)',
'G2626': 'no, not (ouchi)',
'G2627': 'no, not (ouchi)',
'G2628': 'from where, whence (ophthe)',
'G2629': 'an eye (ophthalmos)',
'G2630': 'eye-service (ophthalmodouleia)',
'G2631': 'a serpent (ophis)',
'G2632': 'eyewitness (ophth)',
'G2633': 'eyewitness (ophth)',
'G2634': 'an eyebrow (ophrus)',
'G2635': 'a city (polis)',
'G2636': 'tail (oura)',
'G2637': 'ear (ous)',
'G2638': 'substance, property (ousia)',
'G2639': 'not, no (oute)',
'G2640': 'this (houtos)',
'G2641': 'this (houtos)',
'G2642': 'in this way, thus (houto)',
'G2643': 'so, thus (houtos)',
'G2644': 'no, not (ouchi)',
'G2645': 'no, not (ouchi)',
'G2646': 'from where, whence (ophthe)',
'G2647': 'an eye (ophthalmos)',
'G2648': 'eye-service (ophthalmodouleia)',
'G2649': 'a serpent (ophis)',
'G2650': 'eyewitness (ophth)',
'G2651': 'eyewitness (ophth)',
'G2652': 'an eyebrow (ophrus)',
'G2653': 'a city (polis)',
'G2654': 'tail (oura)',
'G2655': 'ear (ous)',
'G2656': 'substance, property (ousia)',
'G2657': 'not, no (oute)',
'G2658': 'this (houtos)',
'G2659': 'this (houtos)',
'G2660': 'in this way, thus (houto)',
'G2661': 'so, thus (houtos)',
'G2662': 'no, not (ouchi)',
'G2663': 'no, not (ouchi)',
'G2664': 'from where, whence (ophthe)',
'G2665': 'an eye (ophthalmos)',
'G2666': 'eye-service (ophthalmodouleia)',
'G2667': 'a serpent (ophis)',
'G2668': 'eyewitness (ophth)',
'G2669': 'eyewitness (ophth)',
'G2670': 'an eyebrow (ophrus)',
'G2671': 'a city (polis)',
'G2672': 'tail (oura)',
'G2673': 'ear (ous)',
'G2674': 'substance, property (ousia)',
'G2675': 'not, no (oute)',
'G2676': 'this (houtos)',
'G2677': 'this (houtos)',
'G2678': 'in this way, thus (houto)',
'G2679': 'so, thus (houtos)',
'G2680': 'no, not (ouchi)',
'G2681': 'no, not (ouchi)',
'G2682': 'from where, whence (ophthe)',
'G2683': 'an eye (ophthalmos)',
'G2684': 'eye-service (ophthalmodouleia)',
'G2685': 'a serpent (ophis)',
'G2686': 'eyewitness (ophth)',
'G2687': 'eyewitness (ophth)',
'G2688': 'an eyebrow (ophrus)',
'G2689': 'a city (polis)',
'G2690': 'tail (oura)',
'G2691': 'ear (ous)',
'G2692': 'substance, property (ousia)',
'G2693': 'not, no (oute)',
'G2694': 'this (houtos)',
'G2695': 'this (houtos)',
'G2696': 'in this way, thus (houto)',
'G2697': 'so, thus (houtos)',
'G2698': 'no, not (ouchi)',
'G2699': 'no, not (ouchi)',
'G2700': 'from where, whence (ophthe)',
'G2701': 'an eye (ophthalmos)',
'G2702': 'eye-service (ophthalmodouleia)',
'G2703': 'a serpent (ophis)',
'G2704': 'eyewitness (ophth)',
'G2705': 'eyewitness (ophth)',
'G2706': 'an eyebrow (ophrus)',
'G2707': 'a city (polis)',
'G2708': 'tail (oura)',
'G2709': 'ear (ous)',
'G2710': 'substance, property (ousia)',
'G2711': 'not, no (oute)',
'G2712': 'this (houtos)',
'G2713': 'this (houtos)',
'G2714': 'in this way, thus (houto)',
'G2715': 'so, thus (houtos)',
'G2716': 'no, not (ouchi)',
'G2717': 'no, not (ouchi)',
'G2718': 'from where, whence (ophthe)',
'G2719': 'an eye (ophthalmos)',
'G2720': 'eye-service (ophthalmodouleia)',
'G2721': 'a serpent (ophis)',
'G2722': 'eyewitness (ophth)',
'G2723': 'eyewitness (ophth)',
'G2724': 'an eyebrow (ophrus)',
'G2725': 'a city (polis)',
'G2726': 'tail (oura)',
'G2727': 'ear (ous)',
'G2728': 'substance, property (ousia)',
'G2729': 'not, no (oute)',
'G2730': 'this (houtos)',
'G2731': 'this (houtos)',
'G2732': 'in this way, thus (houto)',
'G2733': 'so, thus (houtos)',
'G2734': 'no, not (ouchi)',
'G2735': 'no, not (ouchi)',
'G2736': 'from where, whence (ophthe)',
'G2737': 'an eye (ophthalmos)',
'G2738': 'eye-service (ophthalmodouleia)',
'G2739': 'a serpent (ophis)',
'G2740': 'eyewitness (ophth)',
'G2741': 'eyewitness (ophth)',
'G2742': 'an eyebrow (ophrus)',
'G2743': 'a city (polis)',
'G2744': 'tail (oura)',
'G2745': 'a boast (properly, the object (kau-khay-mah)',
'G2746': 'boasting (properly, the act (kau-khay-sis)',
'G2747': 'Cenchreae, a port of Corinth (keng-khreh-ai)',
'G2748': 'Cedron (i.e. Kidron), a brook near Jerusalem (ked-rone)',
'G2749': 'to lie outstretched (kei-mai)',
'G2750': 'a swathe, i.e. winding-sheet (kei-ree-ah)',
'G2751': 'to shear (kei-ro)',
'G2752': 'a cry of incitement (kel-yoo-mah)',
'G2753': '"hail", to incite by word, i.e. order (kel-yoo-o)',
'G2754': 'empty glorying, i.e. self-conceit (ken-od-ox-ee-ah)',
'G2755': 'vainly glorifying, i.e. self-conceited (ken-od-ox-os)',
'G2756': 'empty (ken-os)',
'G2757': 'empty sounding, i.e. fruitless discussion (ken-of-o-nee-ah)',
'G2758': 'to make empty (ken-oh-o)',
'G2759': 'a sting (poisonous) (ken-tron)',
'G2760': 'a centurion, i.e. captain of one hundred soldiers (ken-too-ree-own)',
'G2761': 'vainly, i.e. to no purpose (ken-oce)',
'G2762': 'something horn-like (ker-ai-ah)',
'G2763': 'a potter (ker-am-yooce)',
'G2764': 'made of clay, i.e. earthen (ker-am-ik-os)',
'G2765': 'an earthenware vessel, i.e. jar (ker-am-ee-on)',
'G2766': 'earthenware, i.e. a tile (by analogy, a thin roof or awning) (ker-am-os)',
'G2767': 'to mingle (ker-an-noo-mee)',
'G2768': 'a horn (ker-as)',
'G2769': 'something horned (ker-at-ee-on)',
'G2770': 'to gain (ker-dai-no)',
'G2771': 'gain (financial or genitive case) (ker-dos)',
'G2772': 'a clipping (bit) (ker-mah)',
'G2773': 'a handler of coins, i.e. money-broker (ker-mat-is-tace)',
'G2774': 'a principal thing, i.e. main point (kef-al-ai-on)',
'G2775': '(specially) to strike on the head (kef-al-ai-oh-o)',
'G2776': 'the head (as the part most readily taken hold of) (kef-al-ay)',
'G2777': '(properly) a knob (kef-al-is)',
'G2778': '(properly) an enrollment ("census") (kayn-sos)',
'G2779': 'a garden (kay-pos)',
'G2780': 'a garden-keeper, i.e. gardener (kay-pou-ros)',
'G2781': 'a cell for honey (kay-ree-on)',
'G2782': 'a proclamation (especially of the gospel) (kay-roog-mah)',
'G2783': 'a herald, i.e. of divine truth (especially of the gospel) (kay-roox)',
'G2784': 'to herald (as a public crier), especially divine truth (the gospel) (kay-roos-so)',
'G2785': 'a huge fish (as gaping for prey) (kay-tos)',
'G2786': 'the Rock (kay-fas)',
'G2787': 'a box, i.e. the sacred ark and that of Noah (kib-o-tos)',
'G2788': 'a lyre (kith-ar-ah)',
'G2789': 'to play on a lyre (kith-ar-id-zo)',
'G2790': 'a lyre-singer(-player), i.e. harpist (kith-ar-o"-dos)',
'G2791': 'Cilicia, a region of Asia Minor (kil-ik-ee-ah)',
'G2792': 'cinnamon (kin-am-o-mon)',
'G2793': 'to undergo peril (kin-doon-yoo-o)',
'G2794': 'danger (kin-doo-nos)',
'G2795': 'to stir (transitively) (kin-eh-o)',
'G2796': 'a stirring (kin-ay-sis)',
'G2797': 'Cis (i.e. Kish), an Israelite (kis)',
'G2798': 'a twig or bough (as if broken off) (klad-os)',
'G2799': 'to sob, i.e. wail aloud (klai-o)',
'G2800': 'fracture (the act) (klas-is)',
'G2801': 'a piece (bit) (klas-mah)',
'G2802': 'Claude, an island near Crete (klau-day)',
'G2803': 'Claudia, a Christian woman (klau-dee-ah)',
'G2804': 'Claudius, the name of two Romans (klau-dee-os)',
'G2805': 'lamentation (klauth-mos)',
'G2806': 'to break (specially, of bread) (klah-o)',
'G2807': 'a key (as shutting a lock) (kleis)',
'G2808': 'to close (klei-o)',
'G2809': 'stealing (properly, the thing stolen, but used of the act) (klem-mah)',
'G2810': 'Cleopas, a Christian (kleh-op-as)',
'G2811': 'renown (as if being called) (kleh-os)',
'G2812': 'a stealer, a thief (klep-tace)',
'G2813': 'to filch (klep-to)',
'G2814': 'a limb or shoot (as if broken off) (klay-mah)',
'G2815': 'merciful (klay-mace)',
'G2816': 'to be an heir to (klay-ron-om-eh-o)',
'G2817': 'heirship (klay-ron-om-ee-ah)',
'G2818': 'a sharer by lot, i.e. inheritor (klay-ron-om-os)',
'G2819': 'a die (for drawing chances) (klay-ros)',
'G2820': 'to allot (klay-roh-o)',
'G2821': 'a calling (klay-sis)',
'G2822': 'called (klay-tos)',
'G2823': 'an earthen pot used for baking in (klib-an-os)',
'G2824': 'a slope (klee-mah)',
'G2825': 'a couch (for sleep, sickness, sitting or eating) (klee-nay)',
'G2826': 'a pallet or little couch (klin-id-ee-on)',
'G2827': 'to slant or slope, i.e. incline or decline (klee-no)',
'G2828': '(properly) reclination (klee-see-ah)',
'G2829': 'stealing (klop-ay)',
'G2830': 'a surge of the sea (kloo-down)',
'G2831': 'to surge (kloo-do-nid-zom-ai)',
'G2832': 'Clopas, an Israelite (klo-pas)',
'G2833': 'to scratch (knay-tho)',
'G2834': 'Cnidus, a place in Asia Minor (knee-dos)',
'G2835': 'a quadrans, i.e. a fourth part of the coin called an as (kod-ran-tace)',
'G2836': 'a cavity (koy-lee-ah)',
'G2837': 'to put to sleep (koy-mah-o)',
'G2838': 'sleeping (koy-may-sis)',
'G2839': 'common (koy-nos)',
'G2840': 'to make (or consider) profane (ceremonially) (koy-noh-o)',
'G2841': 'to share with others (objectively or subjectively) (koy-no-neh-o)',
'G2842': 'partnership (koy-nown-ee-ah)',
'G2843': 'communicative (koy-no-nee-kos)',
'G2844': 'a sharer, i.e. associate (koy-no-nos)',
'G2845': 'a couch (koy-tay)',
'G2846': 'a bedroom (koy-tone)',
'G2847': 'crimson-colored (kok-kee-nos)',
'G2848': 'a kernel of seed (kok-kos)',
'G2849': '(properly) to curtail (kol-ad-zo)',
'G2850': 'flattery (kol-ak-ei-ah)',
'G2851': 'penal infliction (kol-as-is)',
'G2852': 'to rap with the fist (kol-af-id-zo)',
'G2853': 'to glue (kol-lah-o)',
'G2854': '(properly) a poultice (as made of or in the form of crackers) (kol-lou-ree-on)',
'G2855': 'a coin-dealer (kol-loo-bis-tace)',
'G2856': 'to dock (kol-ob-oh-o)',
'G2857': 'Colossae, a place in Asia Minor (kol-os-sai)',
'G2858': 'a Colossaean, i.e. inhabitant of Colossae (kol-os-sa-yoos)',
'G2859': 'the bosom (kol-pos)',
'G2860': 'to plunge into water (kol-oom-bah-o)',
'G2861': 'a diving-place, i.e. pond for bathing (or swimming) (kol-oom-bay-thrah)',
'G2862': 'a Roman "colony" for veterans (kol-o-nee-ah)',
'G2863': 'to wear tresses of hair (kom-ah-o)',
'G2864': 'the hair of the head (locks) (kom-ay)',
'G2865': '(properly) to provide for (kom-id-zo)',
'G2866': '(figuratively) convalescent, getting better (komp-sot-er-on)',
'G2867': 'to whitewash (kon-ee-ah-o)',
'G2868': 'pulverulence (as blown about) (kon-ee-or-tos)',
'G2869': 'to tire (kop-ad-zo)',
'G2870': 'mourning (properly, by beating the breast) (kop-et-os)',
'G2871': 'cutting, i.e. carnage (kop-ay)',
'G2872': 'to feel fatigue (kop-ee-ah-o)',
'G2873': 'a cut (kop-os)',
'G2874': 'manure (kop-ree-ah)',
'G2875': 'to "chop" (kop-to)',
'G2876': 'a crow (from its voracity) (kor-ax)',
'G2877': 'a (little) girl (kor-as-ee-on)',
'G2878': 'a votive offering and the offering (kor-ban)',
'G2879': 'Core (i.e. Korach), an Israelite (kor-eh)',
'G2880': 'to cram, i.e. glut or sate (kor-en-noo-mee)',
'G2881': 'a Corinthian, i.e. inhabitant of Corinth (kor-in-thee-os)',
'G2882': 'Corinthus, a city of Greece (kor-in-thos)',
'G2883': 'Cornelius, a Roman (kor-nay-lee-os)',
'G2884': 'a cor, i.e. a specific measure (kor-os)',
'G2885': 'to put in proper order, i.e. decorate (kos-meh-o)',
'G2886': 'worldy ("cosmic") (kos-mee-kos)',
'G2887': 'orderly, i.e. decorous (kos-mee-os)',
'G2888': 'a world-ruler, an epithet of Satan (kos-mok-rat-ore)',
'G2889': 'orderly arrangement, i.e. decoration (kos-mos)',
'G2890': 'Quartus, a Christian (kou-ar-tos)',
'G2891': 'cumi (i.e. rise!) (kou-mee)',
'G2892': '"custody", i.e. a Roman sentry (kous-to-dee-ah)',
'G2893': 'to unload (kou-fid-zo)',
'G2894': 'a (small) basket (kof-ee-nos)',
'G2895': 'a mattress (krab-bat-os)',
'G2896': '(properly) to "croak" (as a raven) (krad-zo)',
'G2897': '(properly) a headache (as a seizure of pain) from drunkenness (krai-pal-ay)',
'G2898': 'a skull ("cranium") (kran-ee-on)',
'G2899': 'a margin (kras-ped-on)',
'G2900': 'powerful (krat-ai-os)',
'G2901': 'to empower (krat-ai-oh-o)',
'G2902': 'to use strength, i.e. seize or retain (krat-eh-o)',
'G2903': 'strongest (krat-is-tos)',
'G2904': 'vigor ("great") (krat-os)',
'G2905': 'to clamor (krau-gad-zo)',
'G2906': 'an outcry (in notification, tumult or grief) (krau-gay)',
'G2907': '(butchers) meat (krehas)',
'G2908': '(as noun) better, i.e. greater advantage (krice-son)',
'G2909': 'stronger (kreit-town)',
'G2910': 'to hang (krem-an-noo-mee)',
'G2911': 'overhanging, i.e. a precipice (krame-nos)',
'G2912': 'a Cretan, i.e. inhabitant of Crete (krays)',
'G2913': 'growing (krace-kace)',
'G2914': 'Crete, an island in the Mediterranean (kray-tay)',
'G2915': 'barley (kree-thay)',
'G2916': 'consisting of barley (kree-thee-nos)',
'G2917': 'a decision (the function or the effect, for or against ("crime")) (kree-mah)',
'G2918': 'a lily (kree-non)',
'G2919': '(properly) to distinguish, i.e. decide (mentally or judicially) (kree-no)',
'G2920': 'decision (subjectively or objectively, for or against) (kree-sis)',
'G2921': '"crisp" (kris-pos)',
'G2922': 'a rule of judging ("criterion") (kree-tay-ree-on)',
'G2923': 'a judge (genitive case or specially) (kree-tace)',
'G2924': 'decisive ("critical"), i.e. discriminative (krit-ee-kos)',
'G2925': 'to rap (krou-o)',
'G2926': 'a hidden place, i.e. cellar ("crypt") (kroop-tay)',
'G2927': 'concealed, i.e. private (kroop-tos)',
'G2928': 'to conceal (properly, by covering) (kroop-to)',
'G2929': 'to make (i.e. intransitively, resemble) ice ("crystallize") (kroos-tal-lid-zo)',
'G2930': 'ice (kroos-tal-los)',
'G2931': 'privately (kroo-fay)',
'G2932': 'to get, i.e. acquire (by any means, to own) (ktah-om-ai)',
'G2933': 'an acquirement, i.e. estate (ktay-mah)',
'G2934': 'property (ktay-nos)',
'G2935': 'an owner (ktay-tore)',
'G2936': 'to fabricate, i.e. found (form originally) (ktid-zo)',
'G2937': 'original formation (ktis-is)',
'G2938': 'an original formation (concretely), i.e. product (created thing) (ktis-mah)',
'G2939': 'a founder, i.e. God (as author of all things) (ktis-tace)',
'G2940': 'gambling (koo-bei-ah)',
'G2941': 'pilotage (koo-ber-nay-sis)',
'G2942': 'helmsman (koo-ber-nay-tace)',
'G2943': 'from the circle, i.e. all around (koo-kloth-en)',
'G2944': 'to encircle, i.e. surround (koo-kloh-o)',
'G2945': 'i.e. in a circle (koo-klo")',
'G2946': 'a wallow (the effect of rolling), i.e. filth (koo-lis-mah)',
'G2947': 'to roll about (koo-lee-oh-o)',
'G2948': 'rocking about, i.e. crippled (maimed, in feet or hands) (kool-los)',
'G2949': 'a billow (as bursting or toppling) (koo-mah)',
'G2950': 'a "cymbal" (as hollow) (koom-bal-on)',
'G2951': 'dill or fennel ("cummin") (koo-min-on)',
'G2952': 'a puppy (koo-nar-ee-on)',
'G2953': 'a Cyprian (Cypriot), i.e. inhabitant of Cyprus (koo-pree-os)',
'G2954': 'Cyprus, an island in the Mediterranean (koo-pros)',
'G2955': 'to bend forward (koop-to)',
'G2956': 'i.e. Cyrenaian, i.e. inhabitant of Cyrene (koo-ray-nai-os)',
'G2957': 'Cyrene, a region of Africa (koo-ray-nay)',
'G2958': 'Cyrenius (i.e. Quirinus), a Roman (koo-ray-nee-os)',
'G2959': 'Cyria, a Christian woman (koo-ree-ah)',
'G2960': 'belonging to the Lord (Jehovah or Jesus) (koo-ree-ak-os)',
'G2961': 'to rule (koo-ree-yoo-o)',
'G2962': 'supreme in authority (koo-ree-os)',
'G2963': 'mastery (koo-ree-ot-ace)',
'G2964': 'to make authoritative, i.e. ratify (koo-roh-o)',
'G2965': 'a dog ("hound") (koo-own)',
'G2966': 'a limb of the body (as if lopped) (ko-lon)',
'G2967': 'to hinder or forbid, i.e. prevent (by act or word) (ko-loo-o)',
'G2968': 'a hamlet (as if laid down) (ko-may)',
'G2969': 'an unwalled city (ko-mop-ol-is)',
'G2970': 'a carousal (as if letting loose) (ko-mos)',
'G2971': 'a mosquito (from its stinging proboscis) (ko-nopes)',
'G2972': 'Cos, an island in the Mediterranean (koce)',
'G2973': 'Cosam (i.e. Kosam) an Israelite (ko-sam)',
'G2974': 'blunted (ko-fos)',
'G2975': 'to lot, i.e. determine (by implication, receive) especially by lot (lang-khan-o)',
'G2976': 'Lazarus (i.e. Elazar), the name of two Israelites (one imaginary) (lad-zar-os)',
'G2977': 'privately (lath-rah)',
'G2978': 'a whirlwind (squall) (lai-laps)',
'G2979': 'to recalcitrate (lak-tid-zo)',
'G2980': 'to talk, i.e. utter words (lal-eh-o)',
'G2981': 'talk (lal-ee-ah)',
'G2982': 'lama (i.e. why) (lam-ah)',
'G2983': '(actively) to take (lam-ban-o)',
'G2984': 'Lamech (i.e. Lemek), a patriarch (lam-ekh)',
'G2985': 'a "lamp" or flambeau (lam-pas)',
'G2986': 'radiant (lam-pros)',
'G2987': 'brilliancy (lam-prot-ace)',
'G2988': 'brilliantly (lam-proce)',
'G2989': 'to shine, i.e. radiate brilliancy (lam-po)',
'G2990': 'to lie hid (lan-than-o)',
'G2991': 'rock-quarried (lax-yoo-tos)',
'G2992': 'a people (lah-os)',
'G2993': 'Laodicia, a place in Asia Minor (lah-od-ik-ei-ah)',
'G2994': 'a Laodicean, i.e. inhabitant of Laodicia (lah-od-ik-yooce)',
'G2995': 'the throat ("larynx") (lar-oogx)',
'G2996': 'Lasaea, a place in Crete (las-ai-ah)',
'G2997': 'to crack open (from a fall) (las-kho)',
'G2998': 'to quarry (lat-om-eh-o)',
'G2999': 'ministration of God, i.e. worship (lat-rei-ah)',
'G3000': 'to minister (to God), i.e. render religious homage (lat-ryoo-o)',


'G3001': 'a vegetable (lakh-an-on)',
'G3002': 'Lebbaeus, a Christian (leb-bai-os)',
'G3003': 'a "legion", i.e. Roman regiment (figuratively) (leg-eh-own)',
'G3004': '(properly) to "lay" forth (leg-o)',
'G3005': 'a remainder (lime-mah)',
'G3006': 'smooth, i.e. "level" (lei-os)',
'G3007': 'to leave (lei-po)',
'G3008': 'to be a public servant (lei-tourg-eh-o)',
'G3009': 'public function (as priest ("liturgy") or almsgiver) (lei-tourg-ee-ah)',
'G3010': 'functional publicly ("liturgic") (lei-tourg-ik-os)',
'G3011': 'a public servant, i.e. a functionary in the Temple or Gospel (lei-tourg-os)',
'G3012': 'a "linen" cloth, i.e. apron (len-tee-on)',
'G3013': 'a flake (lep-is)',
'G3014': 'scaliness, i.e. "leprosy" (lep-rah)',
'G3015': 'scaly, i.e. leprous (a leper) (lep-ros)',
'G3016': 'something scaled (light), i.e. a small coin (lep-ton)',
'G3017': 'Levi, the name of three Israelites (lyoo-ee")',
'G3018': 'Lewis (i.e. Levi), a Christian (lyoo-is")',
'G3019': 'a Levite, i.e. descendant of Levi (lyoo-ee"-tace)',
'G3020': 'Levitic, i.e. relating to the Levites (lyoo-it"-ee-kos)',
'G3021': 'to whiten (lyoo-kai-no)',
'G3022': 'white (lyoo-kos)',
'G3023': 'a "lion" (leh-own)',
'G3024': 'forgetfulness (lay-thay)',
'G3025': 'a trough, i.e. wine-vat (lay-nos)',
'G3026': 'foolish or idle talk, trivial chatter (lay-ros)',
'G3027': 'a robber, bandit, armed thief (lay"-stace)',
'G3028': 'receipt (the act) (lape-sis)',
'G3029': 'much (adverbially) (lee-an)',
'G3030': 'the incense-tree (frankincence) (lib-an-os)',
'G3031': 'frankincense (lib-an-o-tos)',
'G3032': 'a Roman freedman (lib-er-tee-nos)',
'G3033': 'Libye, a region of Africa (lib-oo-ay)',
'G3034': 'to stone to death (lith-ad-zo)',
'G3035': 'stony, i.e. made of stone (lith-ee-nos)',
'G3036': 'to throw stones, i.e. lapidate (lith-ob-ol-eh-o)',
'G3037': 'a stone (lee-thos)',
'G3038': 'stone-strewed, i.e. a tessellated mosaic on which the Roman tribunal was placed (lith-os-tro-tos)',
'G3039': 'to winnow (lik-mah-o)',
'G3040': 'a harbor (lee-mayn)',
'G3041': 'a pond (large or small) (lim-nay)',
'G3042': 'a scarcity of food (lee-mos)',
'G3043': 'flax (lee-non)',
'G3044': 'Linus, a Christian (lee-nos)',
'G3045': 'fat (lip-ar-os)',
'G3046': 'a pound in weight (lee-trah)',
'G3047': 'the south(- west) wind (as bringing rain) (leeps)',
'G3048': 'a contribution (log-ee-ah)',
'G3049': 'to take an inventory, i.e. estimate (log-id-zom-ai)',
'G3050': 'rational ("logical") (log-ik-os)',
'G3051': 'an utterance (of God) (log-ee-on)',
'G3052': 'fluent, i.e. an orator (log-ee-os)',
'G3053': 'computation (log-is-mos)',
'G3054': 'to be disputatious (on trifles) (log-om-akh-eh-o)',
'G3055': 'disputation about trifles ("logomachy") (log-om-akh-ee-ah)',
'G3056': 'something said (including the thought) (log-os)',
'G3057': 'a "lance" (long-khay)',
'G3058': 'to reproach, i.e. vilify (loy-dor-eh-o)',
'G3059': 'slander or vituperation (loy-dor-ee-ah)',
'G3060': 'abusive, i.e. a blackguard (loy-dor-os)',
'G3061': 'a plague (loy-mos)',
'G3062': 'remaining ones (loy-poy)',
'G3063': 'something remaining (adverbially) (loy-pon)',
'G3064': 'remaining time (loy-pou)',
'G3065': 'Lucas, a Christian (lou-kas)',
'G3066': 'illuminative (lou-kee-os)',
'G3067': 'a bath (lou-tron)',
'G3068': 'to bathe (lou-o)',
'G3069': 'Lydda (i.e. Lod), a place in Israel (lud-dah)',
'G3070': 'Lydia, a Christian woman (loo-dee-ah)',
'G3071': 'Lycaonia, a region of Asia Minor (loo-kah-on-ee-ah)',
'G3072': 'Lycaonistically, i.e. in the language of the Lycaonians (loo-kah-on-is-tee)',
'G3073': 'Lycia, a province of Asia Minor (loo-kee-ah)',
'G3074': 'a wolf (loo-kos)',
'G3075': '(properly) to soil (loo-mai-nom-ai)',
'G3076': 'to distress (loo-peh-o)',
'G3077': 'sadness (loo-pay)',
'G3078': 'grief-dispelling (loo-san-ee-as)',
'G3079': 'Lysias, a Roman (loo-see-as)',
'G3080': 'a loosening (loo-sis)',
'G3081': 'impersonally, it answers the purpose, i.e. is advantageous (loo-sit-el-ei)',
'G3082': 'Lystra, a place in Asia Minor (loos-trah)',
'G3083': 'something to loosen with, i.e. a redemption price (loo-tron)',
'G3084': 'to ransom (loo-troh-o)',
'G3085': 'a ransoming (figuratively) (loo-tro-sis)',
'G3086': 'a redeemer (figuratively) (loo-tro-tace)',
'G3087': 'a lamp-stand (lookh-nee-ah)',
'G3088': 'a portable lamp or other illuminator (lookh-nos)',
'G3089': 'to "loosen" (loo-o)',
'G3090': 'Lois, a Christian woman (low-ees")',
'G3091': 'Lot, a patriarch (lote)',
'G3092': 'Maath, an Israelite (mah-ath)',
'G3093': 'the tower (mag-dal-ah)',
'G3094': 'a female Magdalene, i.e. inhabitant of Magdala (mag-dal-ay-nay)',
'G3095': '"magic" (mag-ei-ah)',
'G3096': 'to practice magic (mag-yoo-o)',
'G3097': 'a Magian, i.e. Oriental scientist (mag-os)',
'G3098': 'Magog, a foreign nation (mag-ogue)',
'G3099': 'Madian (i.e. Midian), a region of Arabia (mad-ee-an)',
'G3100': '(intransitively) to become a pupil (math-ayt-yoo-o)',
'G3101': 'a learner, i.e. pupil (math-ay-tays)',
'G3102': 'a female pupil (math-ay-tree-ah)',
'G3103': 'Mathusala (i.e. Methushelach), an antediluvian (pre-flood) (math-ou-sal-ah)',
'G3104': 'Mainan, an Israelite (mai"-nan)',
'G3105': 'to rave as a "maniac" (mai-nom-ai)',
'G3106': 'to beatify, i.e. pronounce (or esteem) fortunate (mak-ar-id-zo)',
'G3107': 'supremely blest (mak-ar-ee-os)',
'G3108': 'beatification, i.e. attribution of good fortune (mak-ar-is-mos)',
'G3109': 'Macedonia, a region of Greece (mak-ed-on-ee-ah)',
'G3110': 'a Macedon (Macedonian), i.e. inhabitant of Macedonia (mak-ed-own)',
'G3111': 'a butchers stall, meat market or provision-shop (mak-el-lon)',
'G3112': 'at a distance (mak-ran)',
'G3113': 'from a distance or afar (mak-roth-en)',
'G3114': 'to be long-spirited (mak-roth-oo-meh-o)',
'G3115': 'longanimity (mak-roth-oo-mee-ah)',
'G3116': 'with long (enduring) temper, i.e. leniently (mak-roth-oo-moce)',
'G3117': 'long (in place (distant) or time (neuter plural)) (mak-ros)',
'G3118': 'long-timed, i.e. long-lived (mak-rokh-ron-ee-os)',
'G3119': 'softness, i.e. enervation (debility) (mal-ak-ee-ah)',
'G3120': 'soft, i.e. fine (clothing) (mal-ak-os)',
'G3121': 'Maleleel (i.e. Mahalalel), an antediluvian (pre-flood) (mal-el-eh-ale)',
'G3122': '(adverbially) most (in the greatest degree) or particularly (mal-is-tah)',
'G3123': '(adverbially) more (in a greater degree)) or rather (mal-lon)',
'G3124': 'Malchus, an Israelite (mal-khos)',
'G3125': 'a grandmother (mam-may)',
'G3126': 'mammonas, i.e. avarice (deified) (mam-mo-nas)',
'G3127': 'Manaen, a Christian (man-ah-ayn)',
'G3128': 'Mannasses (i.e. Menashsheh), an Israelite (man-as-sace)',
'G3129': 'to learn (in any way) (man-than-o)',
'G3130': 'craziness (man-ee-ah)',
'G3131': 'manna (i.e. man), an edible gum (man-nah)',
'G3132': 'to divine, i.e. utter spells (under pretense of foretelling (mant-yoo-om-ai)',
'G3133': 'to extinguish (as fire) (mar-ai-no)',
'G3134': 'maranatha, i.e. an exclamation of the approaching divine judgment (mar-an)',
'G3135': 'a pearl (mar-gar-ee-tace)',
'G3136': 'Martha, a Christian woman (mar-thah)',
'G3137': 'Maria or Mariam (i.e. Mirjam), the name of six Christian females (mar-ee-ah)',
'G3138': 'Marcus, a Christian (mar-kos)',
'G3139': 'marble (as sparkling white) (mar-mar-os)',
'G3140': 'to be a witness, i.e. testify (mar-too-reh-o)',
'G3141': 'evidence given (judicially or genitive case) (mar-too-ree-ah)',
'G3142': 'something evidential (mar-too-ree-on)',
'G3143': 'to be adduced as a witness (mar-too-rom-ai)',
'G3144': 'a witness (mar-toos)',
'G3145': 'to chew (mas-sah-om-ai)',
'G3146': 'to flog (mas-tig-oh-o)',
'G3147': 'to whip (mas-tid-zo)',
'G3148': 'a whip (mas-tix)',
'G3149': 'a (properly, female) breast (as if kneaded up) (mas-tos)',
'G3150': 'random talk, i.e. babble (mat-ai-ol-og-ee-ah)',
'G3151': 'an idle (i.e. senseless or mischievous) talker, i.e. a wrangler (mat-ai-ol-og-os)',
'G3152': 'empty (mat-ai-os)',
'G3153': 'inutility (mat-ai-ot-ace)',
'G3154': 'to render (passively, become) foolish (mat-ai-oh-o)',
'G3155': 'folly (mat-ayn)',
'G3156': 'Matthaeus (i.e. Matthitjah), an Israelite and a Christian (mat-thai-os)',
'G3157': 'Matthan (i.e. Mattan), an Israelite (mat-than)',
'G3158': 'Matthat (i.e. Mattithjah), the name of two Israelites (mat-that)',
'G3159': 'Matthias (i.e. Mattithjah), an Israelite (mat-thee-as)',
'G3160': 'Mattatha (i.e. Mattithjah), an Israelite (mat-tath-ah)',
'G3161': 'Mattathias (i.e. Mattithjah), an Israelite and a Christian (mat-tath-ee-as)',
'G3162': 'a knife, i.e. dirk (makh-ai-rah)',
'G3163': 'a battle (makh-ay)',
'G3164': 'to war (makh-om-ai)',
'G3165': 'me (meh)',
'G3166': 'to talk big, i.e. be grandiloquent (arrogant, egotistic) (meg-al-au-kheh-o)',
'G3167': 'magnificent (meg-al-ei-os)',
'G3168': 'superbness, i.e. glory or splendor (meg-al-ei-ot-ace)',
'G3169': 'befitting greatness or magnificence (majestic) (meg-al-op-rep-ace)',
'G3170': 'to make (or declare) great, i.e. increase or (figuratively) extol (meg-al-oo-no)',
'G3171': 'much (meg-al-oce)',
'G3172': 'greatness (meg-al-o-soo-nay)',
'G3173': 'big (meg-as)',
'G3174': 'magnitude (figuratively) (meg-eth-os)',
'G3175': 'grandees (meg-is-tan-es)',
'G3176': 'greatest or very great (meg-is-tos)',
'G3177': 'to explain over, i.e. translate (meth-er-mayn-yoo-o)',
'G3178': 'an intoxicant (meth-ay)',
'G3179': 'to transfer, i.e. carry away, depose or (figuratively) exchange, seduce (meth-is-tay-mee)',
'G3180': 'travelling over, i.e. travesty (trickery) (meth-od-ei-ah)',
'G3181': 'bounded alongside, i.e. contiguous (neuter plural as noun, frontier) (meth-or-ee-os)',
'G3182': 'to intoxicate (meth-oos-ko)',
'G3183': 'tipsy (meth-oo-sos)',
'G3184': 'to drink to intoxication, i.e. get drunk (meth-oo-o)',
'G3185': '(adverbially) in greater degree (mide-zon)',
'G3186': 'still larger (figuratively) (meid-zot-er-os)',
'G3187': 'larger (specially, in age) (meid-zone)',
'G3188': 'ink (mel-an)',
'G3189': 'black (mel-as)',
'G3190': 'Meleas, an Israelite (mel-eh-as)',
'G3191': 'to take care of (mel-et-ah-o)',
'G3192': 'honey (mel-ee)',
'G3193': 'relating to honey, i.e. bee (comb) (mel-is-see-os)',
'G3194': 'Melita, an island in the Mediterranean (mel-ee-tay)',
'G3195': 'to intend, i.e. be about to be, do, or suffer something (of persons or things, especially events, in the sense of purpose, duty, necessity, probability, possibility, or hesitation) (mel-lo)',
'G3196': 'a limb or part of the body (mel-os)',
'G3197': 'Melchi (i.e. Malki), the name of two Israelites (mel-khee)',
'G3198': 'Melchisedek (i.e. Malkitsedek), a patriarch (mel-khis-ed-ek)',
'G3199': 'to be of interest to, i.e. to concern (only third person singular present indicative used impersonally, it matters) (mel-o)',
'G3200': 'a (written) sheep-skin (mem-bran-ah)','G3201': 'to blame (mem-fom-ai)',
'G3202': 'blaming fate, i.e. querulous (discontented) (mem-psim-oy-ros)',
'G3303': '(properly) indicative of affirmation or concession (in fact) (men)',
'G3304': 'so then at least (men-oun-geh)',
'G3305': 'indeed though, i.e. however (men-toy)',
'G3306': 'to remain (men-o)',
'G3307': 'to part (mer-id-zo)',
'G3308': 'solicitude (mer-im-nah)',
'G3309': 'to be anxious about (mer-im-nah-o)',
'G3310': 'a portion, i.e. province, share or (abstractly) participation (mer-ece)',
'G3311': 'a separation or distribution (mer-is-mos)',
'G3312': 'an apportioner (administrator) (mer-is-tace)',
'G3313': 'a division or share (mer-os)',
'G3314': 'midday (mes-ame-bree-ah)',
'G3315': 'to interpose (as arbiter), i.e (by implication) to ratify (as surety) (mes-it-yoo-o)',
'G3316': 'a go-between (mes-ee-tace)',
'G3317': 'midnight (especially as a watch) (mes-on-ook-tee-on)',
'G3318': 'Mesopotamia (as lying between the Euphrates and the Tigris), a region of Asia (mes-op-ot-am-ee-ah)',
'G3319': 'middle (as an adjective or (neuter) noun) (mes-os)',
'G3320': 'a partition (figuratively) (mes-ot-oy-khon)',
'G3321': 'mid-sky (mes-ou-ran-ay-mah)',
'G3322': 'to form the middle (mes-oh-o)',
'G3323': 'the Messias (i.e. Mashiach), or Christ (mes-see-as)',
'G3324': 'replete (mes-tos)',
'G3325': 'to replenish (mes-toh-o)',
'G3326': '(properly) denoting accompaniment (met-ah)',
'G3327': 'to change place (met-ab-ai-no)',
'G3328': 'to throw over (met-ab-al-lo)',
'G3329': 'to lead over, i.e. transfer (direct) (met-ag-o)',
'G3330': 'to give over, i.e. share (met-ad-id-o-mee)',
'G3331': 'transposition, i.e. transferral (to heaven), disestablishment (of a law) (met-ath-es-is)',
'G3332': 'to betake oneself, i.e. remove (locally) (met-ai-ro)',
'G3333': 'to call elsewhere, i.e. summon (met-ak-al-eh-o)',
'G3334': 'to stir to a place elsewhere, i.e. remove (figuratively) (met-ak-ee-neh-o)',
'G3335': 'to participate (met-al-am-ban-o)',
'G3336': 'participation (met-al-ape-sis)',
'G3337': 'to exchange (met-al-las-so)',
'G3338': 'to care afterwards, i.e. regret (met-am-el-lom-ai)',
'G3339': 'to transform ("metamorphose") (met-am-or-foh-o)',
'G3340': 'to think differently or afterwards, i.e. reconsider (morally, feel compunction) (met-an-o-eh-o)',
'G3341': '(subjectively) compunction (for guilt, including reformation) (met-an-oy-ah)',
'G3342': 'betwixt (of place or person) (met-ax-oo)',
'G3343': 'to send from elsewhere (met-ap-emp-o)',
'G3344': 'to turn across, i.e. transmute or (figuratively) corrupt (met-as-tref-o)',
'G3345': 'to transfigure or disguise (met-askh-ay-mat-id-zo)',
'G3346': 'to transfer (met-at-ith-ay-mee)',
'G3347': 'thereafter (met-ep-ei-tah)',
'G3348': 'to share or participate (met-ekh-o)',
'G3349': 'to raise in mid-air (met-eh-o-rid-zo)',
'G3350': 'a change of abode (met-oy-kes-ee-ah)',
'G3351': 'to transfer as a settler or captive, i.e colonize or exile (met-oy-kid-zo)',
'G3352': 'participation, i.e. intercourse (met-okh-ay)',
'G3353': 'participant (met-okh-os)',
'G3354': 'to measure (i.e. ascertain in size by a fixed standard) (met-reh-o)',
'G3355': 'a measurer (met-ray-tace)',
'G3356': 'to be moderate in passion, i.e. gentle (to treat indulgently) (met-ree-op-ath-eh-o)',
'G3357': 'moderately, i.e. slightly (met-ree-oce)',
'G3358': 'a measure ("metre") (met-ron)',
'G3359': 'the forehead (as opposite the countenance) (met-o-pon)',
'G3360': 'as far as, i.e. up to a certain point (mekh-ree)',
'G3361': '(adverb) not (may)',
'G3362': 'if not, i.e. unless (eh-an)',
'G3363': 'in order (or so) that not (hin-ah)',
'G3364': 'a double negative strengthening the denial, "not at all" (ou)',
'G3365': 'not even one (may-dam-oce)',
'G3366': 'but not, not even (may-deh)',
'G3367': 'not even one (man, woman, thing) (may-deis)',
'G3368': 'not even ever (may-dep-ot-eh)',
'G3369': 'not even yet (may-dep-o)',
'G3370': 'a Median, or inhabitant of Media (may-dos)',
'G3371': 'no further (may-ket-ee)',
'G3372': 'length (may-kos)',
'G3373': 'to lengthen (may-koo-no)',
'G3374': 'a sheep-skin (may-lo-tay)',
'G3375': 'assuredly (mayn)',
'G3376': 'a month (mayn)',
'G3377': 'to disclose (through the idea of mental effort and thus calling to mind), i.e. report, declare, intimate (may-noo-o)',
'G3378': 'as interrogative and negative, is it not that? (may)',
'G3379': 'not ever (may-pot-eh)',
'G3380': 'not yet (may-po)',
'G3381': 'lest somehow (may-poce)',
'G3382': 'a thigh (may-ros)',
'G3383': 'not too (may-teh)',
'G3384': 'a "mother" (may-tare)',
'G3385': 'whether at all (may-tee)',
'G3386': 'not at all then, i.e. not to say (the rather still) (may-tig-eh)',
'G3387': 'whether any (may-tis)',
'G3388': 'the matrix (may-trah)',
'G3389': 'a matricide, mother murderer (may-tral-ow"-as)',
'G3390': 'a mother city, i.e. "metropolis" (may-trop-ol-is)',
'G3391': 'one or first (mee-ah)',
'G3392': 'to sully or taint, i.e. contaminate (ceremonially or morally) (mee-ai-no)',
'G3393': '(morally) foulness (properly, the effect) (mee-as-mah)',
'G3394': '(morally) contamination (properly, the act) (mee-as-mos)',
'G3395': 'a compound (mig-mah)',
'G3396': 'to mix (mig-noo-mee)',
'G3397': 'a small space of time or degree (mik-ron)',
'G3398': 'small (in size, quantity, number or (figuratively) dignity) (mik-ros)',
'G3399': 'Miletus, a city of Asia Minor (mil-ay-tos)',
'G3400': 'a thousand paces, i.e. a "mile" (mil-ee-on)',
'G3401': 'to imitate (mim-eh-om-ai)',
'G3402': 'an imitator (mim-ay-tace)',
'G3403': 'to remind (mim-nace-ko)',
'G3404': 'to hate (mis-eh-o)',
'G3405': 'requital (good or bad) (mis-thap-od-os-ee-ah)',
'G3406': 'a renumerator (mis-thap-od-ot-ace)',
'G3407': 'a wage-earner (mis-thee-os)',
'G3408': 'payment for service (good or bad) (mis-thos)',
'G3409': 'to let out for wages (mis-thoh-o)',
'G3410': 'a rented building (mis-tho-mah)',
'G3411': 'a wage-worker (good or bad) (mis-tho-tos)',
'G3412': 'Mitylene (or Mytilene), a town on the island of Lesbos (mit-oo-lay-nay)',
'G3413': 'Michael, an archangel (mikh-ah-ale)',
'G3414': 'a mna (i.e. mina), a certain weight (mnah)',
'G3415': 'to bear in mind, i.e. recollect (mnah-om-ai)',
'G3416': 'Mnason, a Christian (mnah-sown)',
'G3417': 'recollection (mnei-ah)',
'G3418': 'a memorial, i.e. sepulchral monument (burial-place) (mnay-mah)',
'G3419': 'a remembrance, i.e. cenotaph (place of interment) (mnay-mei-on)',
'G3420': 'memory (mnay-may)',
'G3421': 'to exercise memory, i.e. recollect (mnay-mon-yoo-o)',
'G3422': 'a reminder (memorandum), i.e. record (mnay-mos-oo-non)',
'G3423': 'to give a souvenir (engagement present), i.e. betroth (mnace-tyoo-o)',
'G3424': 'hardly talking, i.e. dumb (tongue-tied) (mog-il-al-os)',
'G3425': 'with difficulty (mog-is)',
'G3426': 'a modius, i.e. certain measure for things dry (the quantity or the utensil) (mod-ee-os)',
'G3427': 'to me (moy)',
'G3428': 'an adulteress (moy-khal-is)',
'G3429': '(middle voice) to commit adultery (moy-khah-o)',
'G3430': 'adultery (moy-khei-ah)',
'G3D31': 'to commit adultery (moy-khyoo-o)',
'G3432': 'a (male) adulterer (moy-khos)',
'G3433': 'with difficulty (mol-is)',
'G3434': 'Moloch (i.e. Molek), an idol (mol-okh)',
'G3435': 'to soil (figuratively) (mol-oo-no)',
'G3436': 'a stain (mol-oos-mos)',
'G3437': 'blame (mom-fay)',
'G3438': 'a staying, i.e. residence (the act or the place) (mon-ay)',
'G3439': 'only-born, i.e. sole (mon-og-en-ace)',
'G3440': 'merely (mon-on)',
'G3441': 'remaining, i.e. sole or single (mon-os)',
'G3442': 'one-eyed (mon-of-thal-mos)',
'G3443': 'to isolate, i.e. bereave (mon-oh-o)',
'G3444': 'shape (mor-fay)',
'G3445': 'to fashion (figuratively) (mor-foh-o)',
'G3446': 'formation (mor-fo-sis)',
'G3447': 'to fabricate the image of a bullock (mos-khop-oy-eh-o)',
'G3448': 'a young bullock (mos-khos)',
'G3449': 'toil (mokh-thos)',
'G3450': 'of me (mou)',
'G3451': '"musical" (mou-sik-os)',
'G3452': 'the marrow (moo-el-os)',
'G3453': 'to initiate (moo-eh-o)',
'G3454': 'a tale, i.e. fiction ("myth") (moo-thos)',
'G3455': 'to bellow (roar) (moo-kah-om-ai)',
'G3456': 'to make mouths at, i.e. ridicule (mook-tay-rid-zo)',
'G3457': 'belonging to a mill (moo-lee-kos)',
'G3458': 'a "mill" (moo-los)',
'G3459': 'a mill-house (moo-lone)',
'G3460': 'Myra, a place in Asia Minor (moo-rah)',
'G3461': 'a ten-thousand (moo-ree-as)',
'G3462': 'to apply (perfumed) ointment to (moo-rid-zo)',
'G3463': 'ten thousand (moo-ree-oi)',
'G3464': '"myrrh" (moo-ron)',
'G3465': 'Mysia, a region of Asia Minor (moo-see-ah)',
'G3466': 'a secret or "mystery" (moos-tay-ree-on)',
'G3467': 'to shut the eyes, i.e. blink (see indistinctly) (moo-ope-ad-zo)',
'G3468': 'a mole ("black eye") or blow-mark (mo-lopes)',
'G3469': 'to carp at, i.e. censure (discredit) (mo-mah-om-ai)',
'G3470': 'a flaw or blot (mo-mos)',
'G3471': 'to become insipid (mo-rai-no)',
'G3472': 'silliness, i.e. absurdity (mo-ree-ah)',
'G3473': 'silly talk, i.e. buffoonery (mo-rol-og-ee-ah)',
'G3474': 'dull or stupid (as if shut up), i.e. heedless (mo-ros)',
'G3475': 'Moseus, Moses, or Mouses (i.e. Mosheh) (moce-yoos)',
'G3476': 'Naasson (i.e. Nachshon), an Israelite (nah-as-sone)',
'G3477': 'Nangae (i.e. perhaps Nogach), an Israelite (nang-gai)',
'G3478': 'Nazareth or Nazaret, a place in Israel (nad-zar-eth)',
'G3479': 'a Nazarene, i.e. inhabitant of Nazareth (nad-zar-ay-nos)',
'G3480': 'a Nazoraean, i.e. inhabitant of Nazareth (nad-zo-rai-os)',
'G3481': 'Nathan, an Israelite (nath-an)',
'G3482': 'Nathanail (i.e. Nathanel), an Israelite and Christian (nath-an-ah-ale)',
'G3483': 'yes (nai)',
'G3484': 'Nain, a place in Israel (nah-in")',
'G3485': '(properly) a dwelling place (nah-os)',
'G3486': 'Naum (i.e. Nachum), an Israelite (nah-oum)',
'G3487': '"nard" (nar-dos)',
'G3488': 'a flower of the same name (nar-kis-sos)',
'G3489': 'to be shipwrecked (stranded, "navigate") (nau-ag-eh-o)',
'G3490': 'a captain (nau-klay-ros)',
'G3491': 'a boat (of any size) (naus)',
'G3492': 'a boatman, i.e. seaman (nau-tace)',
'G3493': 'Nachor, the grandfather of Abraham (nakh-ore)',
'G3494': 'a youth (up to about forty years) (neh-an-ee-as)',
'G3495': 'a youth (under forty) (neh-an-is-kos)',
'G3496': 'new town (neh-ap-ol-is)',
'G3497': 'Neeman (i.e. Naaman), a Syrian (neh-eh-man)',
'G3498': 'dead (literally or figuratively; also as noun) (nek-ros)',
'G3499': 'to deaden, i.e. (figuratively) to subdue (nek-ro-o)',
'G3500': 'decease; figuratively, impotency (nek-ro-sis)',
'G3501': 'nephros (a kidney, the mind)',
'G3502': 'neokoros (a temple keeper)',
'G3503': 'neossos (a young bird)',
'G3504': 'neotes (youth)',
'G3505': 'neophutos (newly planted)',
'G3506': 'Neapolis (Neapolis)',
'G3507': 'Neron (Neron)',
'G3508': 'neuo (to nod, beckon)',
'G3509': 'nephele (a cloud)',
'G3510': 'neo (newly, recently)',
'G3511': 'Nepthalim (Naphtali)',
'G3512': 'Nereus (Nereus)',
'G3513': 'netho (to spin)',
'G3514': 'nepiazo (to be a babe)',
'G3515': 'nepios (an infant, babe)',
'G3516': 'Neri (Neri)',
'G3517': 'nerchomai (to come)',
'G3518': 'nesion (a small island)',
'G3519': 'nesos (an island)',
'G3520': 'nesteia (a fast, fasting)',
'G3521': 'nesteuo (to fast)',
'G3522': 'nestis (fasting, not eating)',
'G3523': 'ne (by)',
'G3524': 'nepho (to be sober, temperate)',
'G3525': 'nephalios (sober, temperate)',
'G3526': 'Niger (Niger)',
'G3527': 'Nikanor (Nicanor)',
'G3528': 'nikao (to overcome, conquer)',
'G3529': 'nike (victory)',
'G3530': 'Nikodemos (Nicodemus)',
'G3531': 'Nikolaites (a Nicolaite)',
'G3532': 'Nikolaos (Nicolaus)',
'G3533': 'Nikopolis (Nicopolis)',
'G3534': 'nikos (victory)',
'G3535': 'Ninos (Nineveh)',
'G3536': 'Nineuites (a Ninevite)',
'G3537': 'nipter (a basin)',
'G3538': 'nipto (to wash)',
'G3539': 'noe (to think)',
'G3540': 'noema (a thought, mind)',
'G3541': 'nothos (a bastard)',
'G3542': 'nome (pasturage, growth)',
'G3543': 'nomizo (to suppose, think)',
'G3544': 'nomikos (pertaining to the law)',
'G3545': 'nomimos (lawfully)',
'G3546': 'nomisma (coin, money)',
'G3547': 'nomodidaskalos (a teacher of the law)',
'G3548': 'nomothesia (legislation)',
'G3549': 'nomotheteo (to legislate, enact)',
'G3550': 'nomothetes (a lawgiver)',
'G3551': 'nomos (a law)',
'G3552': 'noseo (to be sick, dote)',
'G3553': 'nosema (a disease)',
'G3554': 'nosos (a disease)',
'G3555': 'nosphizo (to set apart, purloin)',
'G3556': 'nossia (a brood)',
'G3557': 'nossion (a young bird)',
'G3558': 'notos (the south wind, south)',
'G3559': 'nothros (sluggish, dull)',
'G3560': 'nou (of the mind)',
'G3561': 'nounechos (prudently)',
'G3562': 'NoumPheres (NumPheres)',
'G3563': 'nous (the mind, understanding)',
'G3564': 'nouthesia (admonition)',
'G3565': 'noutheteo (to admonish, warn)',
'G3566': 'Numphas (Nymphas)',
'G3567': 'numphe (a bride, daughter-in-law)',
'G3568': 'numphios (a bridegroom)',
'G3569': 'numphon (a bridal chamber)',
'G3570': 'nun (now, the present)',
'G3571': 'nuni (now, at this time)',
'G3572': 'nustazo (to nod, slumber)',
'G3573': 'nux (night)',
'G3574': 'nucho (to pierce)',
'G3575': 'nothros (sluggish)',
'G3576': 'notos (the back)',
'G3577': 'xenia (hospitality, lodging)',
'G3578': 'xenizo (to lodge, entertain)',
'G3579': 'xenodocheo (to entertain strangers)',
'G3580': 'xenos (a stranger, foreigner)',
'G3581': 'xestes (a pitcher)',
'G3582': 'xeraino (to dry up, wither)',
'G3583': 'xeros (dry, withered)',
'G3584': 'xulinos (wooden)',
'G3585': 'xulon (wood, a tree, cross)',
'G3586': 'xurao (to shave)',
'G3587': 'o (O, oh)',
'G3588': 'ho (the)',
'G3589': 'ogdoekonta (eighty)',
'G3590': 'ogdoos (eighth)',
'G3591': 'ogkos (weight, burden)',
'G3592': 'hode (this, this one)',
'G3593': 'ode (a way, path)',
'G3594': 'hodeuo (to journey)',
'G3595': 'hodegeo (to lead, guide)',
'G3596': 'hodegetes (a leader, guide)',
'G3597': 'hodoiporeo (to journey)',
'G3598': 'hodos (a way, road, journey)',
'G3599': 'odous (a tooth)',
'G3600': 'odunao (to suffer pain, be grieved)',
'G3601': 'odune (pain, sorrow)',
'G3602': 'odurmos (mourning)',
'G3603': 'Ozias (Uzziah)',
'G3604': 'ozo (to stink)',
'G3TwoZeroFive': 'hothen (whence, from where)',
'G3606': 'othone (a sheet, linen cloth)',
'G3607': 'othonion (a linen cloth)',
'G3608': 'oikeios (of the household)',
'G3609': 'oiketes (a household servant)',
'G3610': 'oiketeia (a household of servants)',
'G3611': 'oikeo (to dwell)',
'G3612': 'oikema (a dwelling, prison)',
'G3613': 'oiketerion (a habitation)',
'G3614': 'oikia (a house, household)',
'G3615': 'oikiakos (of the household)',
'G3616': 'oikodespoteo (to rule a house)',
'G3617': 'oikodespotes (a householder)',
'G3618': 'oikodomeo (to build, edify)',
'G3619': 'oikodome (a building, edification)',
'G3620': 'oikodomia (edifying)',
'G3621': 'oikonomeo (to be a steward)',
'G3622': 'oikonomia (stewardship, dispensation)',
'G3623': 'oikonomos (a steward)',
'G3624': 'oikos (a house, household)',
'G3625': 'oikoumene (the inhabited earth)',
'G3626': 'oikouros (a keeper at home)',
'G3627': 'oikteiro (to have compassion)',
'G3628': 'oiktirmos (compassion, mercy)',
'G3629': 'oiktirmon (merciful)',
'G3630': 'oinopotes (a winebibber)',
'G3631': 'oinos (wine)',
'G3632': 'oinophlugia (drunkenness)',
'G3633': 'oiomai (to suppose, think)',
'G3634': 'hoios (what sort of)',
'G3635': 'okneo (to delay, hesitate)',
'G3636': 'okneros (slothful, idle)',
'G3637': 'oktaemeros (on the eighth day)',
'G3638': 'okto (eight)',
'G3639': 'olethros (destruction)',
'G3640': 'oligopistos (of little faith)',
'G3641': 'oligopsuchos (fainthearted)',
'G3642': 'oligos (little, few)',
'G3643': 'oligoreo (to despise, neglect)',
'G3644': 'olothreutes (a destroyer)',
'G3645': 'olothreuo (to destroy)',
'G3646': 'holokautoma (a whole burnt offering)',
'G3647': 'holokleria (perfect soundness)',
'G3648': 'holokleros (whole, entire)',
'G3649': 'ololuzo (to howl)',
'G3650': 'holos (whole, all, complete)',
'G3651': 'holoteles (wholly, completely)',
'G3652': 'Olumpas (Olympas)',
'G3653': 'olunthos (an unripe fig)',
'G3654': 'holos (at all)',
'G3655': 'ombros (a shower)',
'G3656': 'homilia (companionship, converse)',
'G3657': 'omileo (to converse with)',
'G3658': 'homilos (a multitude)',
'G3659': 'omma (an eye)',
'G3660': 'omnumi (to swear, take an oath)',
'G3661': 'homothumadon (with one accord)',
'G3TwoSixTwo': 'homoiazo (to be like)',
'G3663': 'homoiopathes (of like passions)',
'G3664': 'homoios (like, similar)',
'G3665': 'homoiotes (likeness)',
'G3666': 'homoioo (to make like, liken)',
'G3667': 'homoioma (a likeness, form)',
'G3668': 'homoiosis (a likeness)',
'G3669': 'homoios (likewise)',
'G3670': 'homologeo (to confess, profess)',
'G3671': 'homologia (a confession, profession)',
'G3672': 'homologoumenos (confessedly)',
'G3673': 'homotechnos (of the same trade)',
'G3674': 'homou (together)',
'G3675': 'homophron (of one mind)',
'G3676': 'onar (a dream)',
'G3677': 'onarion (a young donkey)',
'G3678': 'oneidizo (to reproach, revile)',
'G3679': 'oneidismos (reproach)',
'G3680': 'oneidos (reproach, disgrace)',
'G3681': 'Onesimos (Onesimus)',
'G3682': 'Onesiphoros (Onesiphorus)',
'G3683': 'onikos (of a donkey)',
'G3684': 'oninemi (to profit, have joy)',
'G3685': 'onoma (a name)',
'G3686': 'onomazo (to name, call by name)',
'G3687': 'onos (a donkey)',
'G3688': 'ontos (really, truly)',
'G3689': 'oxos (sour wine, vinegar)',
'G3690': 'oxus (sharp, swift)',
'G3691': 'ope (a hole, opening)',
'G3692': 'opisthen (behind, after)',
'G3693': 'opiso (behind, after)',
'G3694': 'hoplon (a weapon, instrument)',
'G3695': 'hoplizo (to arm oneself)',
'G3696': 'hopoios (of what sort)',
'G3697': 'hopote (when)',
'G3ThreeEightNineEight': 'hopou (where, whither)',
'G3699': 'optanomai (to appear, be seen)',
'G3700': 'optasia (a vision)',
'G3701': 'optos (cooked, broiled)',
'G3702': 'opora (autumn fruits)',
'G3703': 'hopos (that, in order that)',
'G3704': 'horama (a vision)',
'G3705': 'horasis (sight, a vision)',
'G3706': 'horatos (visible)',
'G3707': 'horao (to see, perceive)',
'G3708': 'orge (wrath, anger)',
'G3709': 'orgizo (to be angry)',
'G3710': 'orgilos (inclined to anger)',
'G3711': 'orguia (a fathom)',
'G3712': 'orego (to desire, long for)',
'G3713': 'oreinos (hilly)',
'G3714': 'orexis (desire, lust)',
'G3715': 'orthopodeo (to walk uprightly)',
'G3716': 'orthos (straight, right)',
'G3717': 'orthotomeo (to rightly divide)',
'G3718': 'orthrizo (to rise early)',
'G3719': 'orthrinos (early in the morning)',
'G3720': 'orthros (dawn, early morning)',
'G3721': 'orthos (rightly, uprightly)',
'G3722': 'horizo (to determine, appoint)',
'G3723': 'horkizo (to adjure, implore)',
'G3724': 'horkos (an oath)',
'G3725': 'horkomosia (an oath)',
'G3726': 'hormao (to rush, set forward)',
'G3727': 'horme (a rush, impulse)',
'G3728': 'hormema (violence)',
'G3729': 'ornon (a bird)',
'G3730': 'ornis (a hen)',
'G3731': 'horothesia (a boundary)',
'G3732': 'oros (a mountain)',
'G3733': 'oros (a boundary)',
'G3734': 'orusso (to dig)',
'G3735': 'orphanos (an orphan)',
'G3736': 'orcheomai (to dance)',
'G3737': 'hos (who, which, what)',
'G3738': 'hosakis (as often as)',
'G3739': 'hosios (holy, pure)',
'G3740': 'hosiotes (holiness)',
'G3741': 'hosos (as great as, as many as)',
'G3742': 'hosios (holily)',
'G3743': 'hosper (as, just as)',
'G3744': 'hosperei (as if, like as)',
'G3745': 'hostis (whoever, whichever)',
'G3746': 'osphresis (the sense of smell)',
'G3747': 'osphus (the loins)',
'G3748': 'hotan (when, whenever)',
'G3749': 'hote (when)',
'G3750': 'hoti (that, because, for)',
'G3751': 'hotou (until, while)',
'G3752': 'hou (where)',
'G3753': 'ou (not)',
'G3754': 'ou (where)',
'G3755': 'ou (of which, whose)',
'G3756': 'ou (not, no)',
'G3757': 'oua (ah!, ha!)',
'G3758': 'ouai (woe!)',
'G3759': 'oudamos (by no means)',
'G3760': 'oude (and not, neither, nor)',
'G3761': 'oudepote (never)',
'G3762': 'oudepo (not yet)',
'G3763': 'oudeis (no one, nothing)',
'G3764': 'oudemia (no one, nothing)',
'G3765': 'ouen (no one, nothing)',
'G3766': 'ouketi (no longer, no more)',
'G3767': 'oun (therefore, then)',
'G3768': 'oupo (not yet)',
'G3769': 'oura (a tail)',
'G3770': 'Ourias (Uriah)',
'G3771': 'ouranos (heaven, the sky)',
'G3772': 'ouranothen (from heaven)',
'G3773': 'Ourbanos (Urbanus)',
'G3774': 'ous (an ear)',
'G3775': 'ousia (substance, property)',
'G3776': 'oute (neither, nor)',
'G3777': 'houtos (this, he, she, it)',
'G3778': 'houto (thus, so, in this manner)',
'G3779': 'ouch (not)',
'G3780': 'ouchi (not, no)',
'G3781': 'opheiletes (a debtor)',
'G3TwoSevenTwo': 'opheile (a debt)',
'G3783': 'opheilema (a debt)',
'G3784': 'opheilo (to owe, be indebted)',
'G3785': 'ophelon (would that!)',
'G3786': 'ophelos (profit, benefit)',
'G3787': 'ophthalmodouleia (eyeservice)',
'G3788': 'ophthalmos (an eye)',
'G3789': 'ophis (a serpent)',
'G3790': 'ophrus (an eyebrow, brow)',
'G3791': 'ochleo (to trouble, vex)',
'G3792': 'ochlopoieo (to gather a crowd)',
'G3793': 'ochlos (a crowd, multitude)',
'G3794': 'ochurosis (fortress)',
'G3795': 'ochuroma (a stronghold)',
'G3796': 'opsarion (a fish)',
'G3797': 'opse (late, at evening)',
'G3798': 'opsimos (late, latter)',
'G3799': 'opsios (late, evening)',
'G3800': 'opsis (the face, appearance)',
'G3801': 'opsonion (wages, provision)',
'G3802': 'pagideuo (to snare, entrap)',
'G3803': 'pagis (a snare, trap)',
'G3804': 'Pagos (Areopagus)',
'G3805': 'pathema (suffering)',
'G3806': 'pathetos (subject to suffering)',
'G3807': 'pathos (passion, lust)',
'G3808': 'paidagogos (a tutor, guardian)',
'G3809': 'paidarion (a little child)',
'G3810': 'paideia (training, discipline)',
'G3811': 'paideuo (to train, discipline, chastise)',
'G3812': 'paideutes (an instructor, corrector)',
'G3813': 'paidiothen (from childhood)',
'G3814': 'paidion (a little child)',
'G3815': 'paidiske (a maidservant)',
'G3816': 'paizo (to play, jest)',
'G3817': 'pais (a child, servant)',
'G3818': 'paio (to strike, smite)',
'G3819': 'Pakatianes (Pacatiana)',
'G3820': 'palai (of old, long ago)',
'G3821': 'palaios (old, ancient)',
'G3822': 'palaiotes (oldness)',
'G3823': 'palaioo (to make old, grow old)',
'GKey824': 'pale (a wrestling, struggle)',
'G3825': 'paliggenesia (regeneration)',
'G3826': 'palin (again, back)',
'G3827': 'pamplethei (all together)',
'G3828': 'pamplous (very great)',
'G3829': 'pampolus (very great)',
'G3830': 'Pamphulia (Pamphylia)',
'G3831': 'pandocheion (an inn)',
'G3832': 'pandocheus (an innkeeper)',
'G3833': 'paneguris (a solemn assembly)',
'G3834': 'panoiki (with the whole house)',
'G3835': 'panoplia (full armor)',
'G3836': 'panourgia (craftiness, cunning)',
'G3837': 'panouros (crafty, cunning)',
'G3838': 'pantachothen (from all sides)',
'G3839': 'pantachou (everywhere)',
'G3840': 'panteles (complete, utter)',
'G3841': 'pante (always)',
'G3842': 'pantothen (from all sides)',
'G3843': 'pantokrator (Almighty)',
'G3844': 'pantote (always, at all times)',
'G3845': 'pantos (in every way, completely)',
'G3846': 'para (from, with, beside)',
'G3847': 'parabaino (to transgress)',
'G3848': 'paraballo (to arrive, compare)',
'G3849': 'parabasis (a transgression)',
'G3850': 'parabates (a transgressor)',
'G3851': 'parabiazomai (to constrain)',
'G3852': 'parabole (a parable, comparison)',
'G3853': 'parabouleuomai (to consult)',
'G3854': 'paraggelia (a command, charge)',
'G3855': 'paraggello (to command, charge)',
'G3856': 'paraginomai (to come, arrive)',
'G3857': 'parago (to pass by)',
'G3858': 'paradeigmatizo (to make a public example)',
'G3859': 'paradeisos (paradise)',
'G3860': 'paradechomai (to receive, accept)',
'G3861': 'paradiatribe (perverse disputing)',
'G3862': 'paradidomi (to deliver up, betray)',
'G3863': 'paradoxos (strange, wonderful)',
'G3864': 'paradosis (a tradition)',
'G3865': 'parazeloo (to provoke to jealousy)',
'G3866': 'parathalassios (by the sea)',
'G3867': 'paratheoreo (to neglect, overlook)',
'G3868': 'paratheke (a deposit)',
'G3869': 'paraineo (to exhort, admonish)',
'G3870': 'paraitomai (to refuse, excuse)',
'G3871': 'parakathizo (to sit down beside)',
'G3872': 'parakaleo (to exhort, comfort)',
'G3873': 'parakalupto (to hide, conceal)',
'G3874': 'paraklesis (exhortation, comfort)',
'G3875': 'parakletos (an advocate, comforter)',
'G3876': 'parakoe (disobedience)',
'G3877': 'parakoloutheo (to follow closely)',
'G3878': 'parakouo (to hear amiss, disobey)',
'G3879': 'parakupto (to stoop down, look into)',
'G3880': 'paralambano (to take, receive)',
'G3881': 'paralegomai (to sail past)',
'G3882': 'paralios (coastal)',
'G3883': 'parallage (change, variation)',
'G3TwoEightFour': 'paralogizomai (to deceive, delude)',
'G3885': 'paraluo (to paralyze, weaken)',
'G3886': 'paralutikos (paralytic)',
'G3887': 'parameno (to remain, continue)',
'G3888': 'paramutheomai (to comfort, console)',
'G3889': 'paramuthia (comfort, consolation)',
'G3890': 'paramuthion (consolation)',
'G3891': 'paranomeo (to act unlawfully)',
'G3892': 'paranomia (transgression)',
'G3893': 'parapikraino (to provoke)',
'G3894': 'parapikrasmos (provocation)',
'G3Comment895': 'parapipto (to fall away)',
'G3896': 'parapleo (to sail by)',
'G3897': 'paraplesion (near to)',
'G3898': 'paraplesios (in like manner)',
'G3899': 'parapoeromai (to go, pass by)',
'G3900': 'paraptoma (a trespass, sin)',
'G3901': 'pararrhueo (to drift away)',
'G3902': 'parasemos (marked)',
'G3903': 'paraskeuazo (to prepare, make ready)',
'G3904': 'paraskeue (preparation)',
'G3905': 'parateino (to extend, prolong)',
'G3906': 'paratereo (to watch, observe)',
'G3907': 'parateresis (observation)',
'G3908': 'paratheke (a deposit)',
'G3909': 'paratithemi (to set before, entrust)',
'G3910': 'paratugchano (to happen to be present)',
'G3911': 'parautika (for a moment)',
'G3912': 'paraphero (to bear away, remove)',
'G3913': 'paraphroneo (to be beside oneself)',
'G3914': 'paraphronia (madness)',
'G3915': 'paracheimazo (to winter)',
'G3916': 'paracheimasia (a wintering)',
'G3917': 'parachrema (immediately)',
'G3918': 'pardalis (a leopard)',
'G3919': 'pareimi (to be present)',
'G3920': 'pareisago (to bring in secretly)',
'G3921': 'pareisaktos (secretly brought in)',
'G3922': 'pareisduno (to creep in unawares)',
'G3923': 'pareiserchomai (to enter secretly)',
'G3924': 'parerchomai (to pass by, pass away)',
'G3925': 'paresis (a passing over, remission)',
'G3926': 'parecho (to offer, present)',
'G3927': 'paregoria (comfort, solace)',
'G3928': 'parthenia (virginity)',
'G3929': 'parthenos (a virgin)',
'G3930': 'Parthos (a Parthian)',
'G3931': 'paristemi (to present, stand by)',
'G3932': 'Parmenios (Parmenios)',
'G3933': 'parodos (a way, passage)',
'G3934': 'paroikeo (to sojourn)',
'G3Examples935': 'paroikia (a sojourning)',
'G3936': 'paroikos (a sojourner, stranger)',
'G3937': 'paroimia (a proverb, parable)',
'G3938': 'paroinos (given to wine)',
'G3939': 'paromoiadzo (to be like)',
'G3940': 'paromoios (like, similar)',
'G3941': 'paroxuno (to provoke, stir up)',
'G3942': 'paroxusmos (a sharp contention, stirring up)',
'G3943': 'parorgizo (to provoke to anger)',
'G3944': 'parorgismos (wrath, anger)',
'G3945': 'parotruno (to stir up, incite)',
'G3946': 'parousia (presence, coming)',
'G3947': 'paropsis (a dish)',
'G3948': 'parrhesia (boldness, confidence)',
'G3949': 'parrhesiadzomai (to speak boldly)',
'G3950': 'parrhesios (boldly)',
'G3951': 'pas (all, every, whole)',
'G3952': 'pascha (Passover)',
'G3953': 'pascho (to suffer)',
'G3954': 'patasso (to strike, smite)',
'G3955': 'pateo (to tread, trample)',
'G3956': 'pater (a father)',
'G3957': 'paternal (from a father)',
'G3958': 'Patmos (Patmos)',
'G3959': 'Patrobas (Patrobas)',
'G3960': 'patroos (of a father, ancestral)',
'G3961': 'patris (fatherland, country)',
'G3962': 'Pauolos (Paul)',
'G3963': 'patria (family, lineage)',
'G3964': 'patriarches (a patriarch)',
'G3965': 'patrikos (fatherly, paternal)',
'G3966': 'patroparadotos (handed down from fathers)',
'G3967': 'patroos (of a father, ancestral)',
'G3968': 'Patara (Patara)',
'G3969': 'pauo (to cease, stop)',
'G3970': 'pachuno (to make fat, dull)',
'G3971': 'pede (a fetter)',
'G3972': 'pedinos (level, plain)',
'G3973': 'pedzeuo (to travel on foot)',
'G3974': 'pedzo (on foot)',
'G3975': 'peitharcheo (to obey authority)',
'G3976': 'peitho (to persuade, trust)',
'G3977': 'peithos (persuasive)',
'G3978': 'peinao (to hunger)',
'G3979': 'peira (a trial, attempt)',
'G3980': 'peirazo (to test, tempt)',
'G3981': 'peirasmos (a temptation, trial)',
'G3982': 'peirao (to attempt)',
'G3983': 'peismone (persuasion)',
'G3984': 'pelagos (the sea)',
'G3985': 'pelekizo (to behead)',
'G3986': 'pelikos (how great, how large)',
'G3987': 'pempo (to send)',
'G3988': 'pemphthos (fifth)',
'G3Examples989': 'penes (poor)',
'G3990': 'penthera (a mother-in-law)',
'G3991': 'pentheros (a father-in-law)',
'G3992': 'pentheo (to mourn, lament)',
'G3993': 'penthos (mourning, sorrow)',
'G3994': 'pentichros (wretched)',
'G3995': 'pentakis (five times)',
'G3996': 'pentakischilioi (five thousand)',
'G3997': 'pentakosioi (five hundred)',
'G3998': 'pente (five)',
'G3999': 'pentekaidekatos (fifteenth)',
'G4000': 'pentekoste (Pentecost)',
'G4001': 'to abstain from (peitharcheo)',
'G4002': 'to be obedient (peithos)',
'G4003': 'persuasive (peinao)',
'G4004': 'to hunger (peira)',
'G4005': 'a trial, experiment (peirazo)',
'G4006': 'to test, tempt (peirasmos)',
'G4007': 'a testing, temptation (peirates)',
'G4008': 'a pirate, robber (peiro)',
'G4009': 'to attempt (peismone)',
'G4010': 'persuasion (pelagos)',
'G4011': 'the sea (pelekizo)',
'G4012': 'to behead (pemphis)',
'G4013': 'blame (pempo)',
'G4014': 'to send (penes)',
'G4015': 'poor (penichros)',
'G4016': 'poor (pentheo)',
'G4017': 'to mourn (penthera)',
'G4018': 'a mother in law (pentheros)',
'G4019': 'a father in law (penthos)',
'G4020': 'mourning (pentakis)',
'G4021': 'five times (pentakischilioi)',
'G4022': 'five thousand (pentakosioi)',
'G4023': 'five hundred (pente)',
'G4024': 'five (pentekaidekatos)',
'G4025': 'fifteenth (pentekonta)',
'G4026': 'fifty (pentekoste)',
'G4027': 'Pentecost (pepoithesis)',
'G4028': 'confidence (per)',
'G4029': 'though, indeed (pera)',
'G4030': 'beyond (perai)',
'G4031': 'beyond (perain)',
'G4032': 'on the other side (peran)',
'G4033': 'beyond (peras)',
'G4034': 'an end (peraste)',
'G4035': 'Pergamum (pergamum)',
'G4036': 'Perga (perge)',
'G4037': 'about, concerning (peri)',
'G4038': 'to bring around (periago)',
'G4039': 'to take away from around (periaireo)',
'G4040': 'to cast a gleam around (periastrapto)',
'G4041': 'to put around (periballo)',
'G4042': 'to look around (periblepo)',
'G4043': 'a covering (peribole)',
'G4044': 'to break off around (perideo)',
'G4045': 'to walk around (periergazomai)',
'G4046': 'to be a busybody (periergos)',
'G4047': 'curious, a busybody (perierchomai)',
'G4048': 'to go about (periecho)',
'G4049': 'to surround, contain (perizoma)',
'G4050': 'a girdle (perizonnumi)',
'G4051': 'to gird about (perithesis)',
'G4052': 'a putting on (periistemi)',
'G4053': 'to stand around, avoid (perikatharma)',
'G4054': 'offscouring, filth (perikalypto)',
'G4055': 'to cover around (perikeimai)',
'G4056': 'to lie around (perikephalaia)',
'G4057': 'a helmet (perikratos)',
'G4058': 'having power over (perikrypto)',
'G4059': 'to hide (perikyloo)',
'G4060': 'to encircle (perilampo)',
'G4061': 'to shine around (perileipo)',
'G4062': 'to leave remaining (perilypos)',
'G4063': 'very sad (perimeno)',
'G4064': 'to wait for (perix)',
'G4065': 'around (perioikeo)',
'G4066': 'to dwell around (perioikos)',
'G4067': 'a neighbor (periousios)',
'G4068': 'peculiar (perioche)',
'G4069': 'a passage of Scripture (peripateo)',
'G4070': 'to walk (peripeiro)',
'G4071': 'to pierce through (peripipto)',
'G4072': 'to fall into (peripoieomai)',
'G4073': 'to preserve, purchase (peripoiesis)',
'G4074': 'preservation, possession (perirrhegnumi)',
'G4075': 'to tear off all around (perispao)',
'G4076': 'to be drawn away, distracted (perisseia)',
'G4077': 'abundance (perisseuma)',
'G4078': 'an abundance (perisseuo)',
'G4079': 'to abound (perissos)',
'G4080': 'abundant (perissoteros)',
'G4081': 'more abundantly (perissos)',
'G4082': 'more abundantly (peristera)',
'G4083': 'a dove (peritemno)',
'G4084': 'to circumcise (peritithemi)',
'G4085': '(to place around (peritome)',
'G4086': 'circumcision (peritrepo)',
'G4087': 'to turn about (peritrecho)',
'G4088': 'to run around (periphero)',
'G4089': 'to carry about (periphroneo)',
'G4090': 'to be overproud (perichoros)',
'G4091': 'surrounding country (peripsao)',
'G4092': 'to wipe off (peripsoma)',
'G4093': 'offscouring (pernao)',
'G4094': 'to sell (perperenomai)',
'G4095': 'to boast (Persis)',
'G4096': 'Persis (persikos)',
'G4097': 'Persian (perusi)',
'G4098': '(last year (petalos)',
'G4099': 'a leaf (petanomai)',
'G4100': 'to fly (peteinon)',
'G4101': 'a bird (petomai)',
'G4102': 'to fly (petra)',
'G4103': 'a rock (petros)',
'G4104': 'Peter (petrodes)',
'G4105': 'rocky (pegnumi)',
'G4106': 'to fasten (pege)',
'G4107': 'a fountain (pedaleo)',
'G4108': 'to steer (pedalion)',
'G4109': 'a rudder (pezeuo)',
'G4110': 'to go by land (peze)',
'G4111': 'on foot (pezos)',
'G4112': 'on foot (pelekus)',
'G4113': 'an axe (pelikos)',
'G4114': 'how great, how old (pelos)',
'G4115': 'clay (pera)',
'G4116': 'a leather pouch (peran)',
'G4117': 'beyond (peras)',
'G4118': 'a limit (perasi)',
'G4119': 'in (pi)',
'G4120': 'Pi (piazo)',
'G4121': 'to lay hold of (piezo)',
'G4122': 'to press down (pithanologia)',
'G4123': 'persuasive speech (pithos)',
'G4124': 'persuasive (pikraino)',
'G4125': 'to make bitter (pikria)',
'G4126': 'bitterness (pikros)',
'G4127': 'bitter (pikros)',
'G4128': 'bitterly (Pilatos)',
'G4129': 'Pilate (pimplamai)',
'G4130': 'to fill (pimpremi)',
'G4131': 'to burn (pinakidion)',
'G4132': 'a tablet (pinax)',
'G4133': 'a platter, tablet (pino)',
'G4134': 'to drink (piotes)',
'G4135': 'fatness (piprasko)',
'G4136': 'to sell (pipto)',
'G4137': 'to fall (Pisidia)',
'G4138': 'Pisidia (Pisidios)',
'G4139': 'Pisidian (pisteuo)',
'G4140': 'to believe (pistikos)',
'G4141': 'genuine, pure (pistis)',
'G4142': 'faith, belief (pistos)',
'G4143': 'faithful, believing (pistoo)',
'G4144': 'to be convinced (planao)',
'G4145': 'to lead astray (plane)',
'G4146': 'a wandering (planetes)',
'G4147': 'a wanderer (planos)',
'G4148': 'an impostor (plax)',
'G4149': 'a tablet (plasma)',
'G4150': 'that which is molded (plasso)',
'G4151': 'to mold (plastos)',
'G4152': 'fabricated (plateia)',
'G4153': 'a street (platos)',
'G4154': 'breadth (platuno)',
'G4155': 'to broaden (platus)',
'G4156': 'broad (plegma)',
'G4157': 'a braid (plege)',
'G4158': 'Way (a blow, wound (plethos)',
'G4159': 'a multitude (plethuno)',
'G4160': 'to multiply (pletho)',
'G4161': 'to fill (plektos)',
'G4162': 'braided (plemone)',
'G4163': 'fullness (plen)',
'G4164': 'but, except (pleres)',
'G4165': 'full (plerophoreo)',
'G4166': 'to fully assure (plerophoria)',
'G4167': 'full assurance (pleroo)',
'G4168': 'to fill (pleroma)',
'G4169': 'fullness (plesion)',
'G4170': 'near (plesmone)',
'G4171': 'indulgence (plesso)',
'G4172': 'to strike (pleura)',
'G4173': 'the side (pleo)',
'G4174': 'to sail (pleonazo)',
'G4175': '(to abound (pleonekteo)',
'G4176': 'to take advantage of (pleonektes)',
'G4177': 'a covetous person (pleonexia)',
'G4178': 'covetousness (ploe)',
'G4179': 'a ship (ploion)',
'G4180': 'a boat (ploos)',
'G4181': 'a voyage (plousios)',
'G4182': 'rich (plousios)',
'G4183': 'richly (plouteo)',
'G4184': 'to be rich (ploutizo)',
'G4185': 'to make rich (ploutos)',
'G4186': 'riches (pluno)',
'G4187': 'to wash (pneuma)',
'G4188': 'spirit, wind (pneumatikos)',
'G4189': 'spiritual (pneumatikos)',
'G4190': 'spiritually (pneo)',
'G4191': 'to blow (pnigo)',
'G4192': 'to choke (pniktos)',
'G4193': 'strangled (pnoe)',
'G4194': 'wind, breath (podere)',
'G4195': 'a long robe (podes)',
'G4196': 'feet (poema)',
'G4197': 'a work, workmanship (poeisis)',
'G4198': 'a doing (poietes)',
'G4199': 'a doer, a poet (poikilos)',
'G4200': 'varied, manifold (poimaino)',
'G4201': 'to shepherd (poimen)',
'G4202': 'a shepherd (poimne)',
'G4203': 'a flock (poimnion)',
'G4204': 'a little flock (poios)',
'G4205': 'what kind? (polemeo)',
'G4206': 'to wage war (polemos)',
'G4207': 'war (polis)',
'G4208': 'a city (politarches)',
'G4209': 'a ruler of a city (politeia)',
'G4210':  '(citizenship (politeuma)',
'G4211': 'commonwealth, citizenship (politeuomai)',
'G4212': 'to be a citizen (polites)',
'G4213': 'a citizen (pollakis)',
'G4214': 'often (pollaplasion)',
'G4215': 'many times more (polulogia)',
'G4216': '(much speaking (polumeros)',
'G4217': 'in many parts (polupoikilos)',
'G4218': 'many colored (polus)',
'G4219': 'much, many (polusplagchnos)',
'G4220': 'very compassionate (poluteles)',
'G4221': 'very costly (polutimos)',
'G4222': 'very precious (polutropos)',
'G4223': 'in many ways (poma)',
'G4224': 'a drink (poneo)',
'G4225': 'to toil (poneria)',
'G4226': 'wickedness (poneros)',
'G4227': '(evil, wicked (poneros)',
'G4228': 'wickedly (ponos)',
'G4229': 'toil, pain (Pontikos)',
'G4230': '(of Pontus (Pontos)',
'G4231': 'Pontus (Poplios)',
'G4232': 'Publius (poreia)',
'G4233': 'a journey (poreuomai)',
'G4234': 'to go, travel (portheo)',
'G4235': 'to destroy (porismos)',
'G4236': 'gain (Porkios)',
'G4237': 'Porcius (porne)',
'G4238': 'a prostitute (porneia)',
'G4239': 'fornication (porneuo)',
'G4240': 'to commit fornication (pornos)',
'G4241': 'a fornicator (porro)',
'G4242': 'far off (porrothen)',
'G4243': 'from afar (porrotero)',
'G4244': 'further (porphura)',
'G4245': 'purple (porphureos)',
'G4246': 'purple (porphuropolis)',
'G4247': 'a seller of purple (posakis)',
'G4248': '(how many times? (posis)',
'G4249': 'a drink (posos)',
'G4250': 'how great, how much (potamos)',
'G4251': 'a river (potamophoretos)',
'G4252': 'carried away by a river (potapos)',
'G4253': 'what kind of? (pote)',
'G4254': 'when? (pote)',
'G4255': 'at some time, once (poteron)',
'G4256': 'whether (poterion)',
'G4257': 'a cup (potizo)',
'G4258': 'to give to drink (potos)',
'G4259': 'a drinking party (Pou)',
'G4260': 'where? (Poudes)',
'G4261': 'Pudens (pous)',
'G4263': 'Player (the foot (pragma)',
'G4263': 'a deed, matter (pragmateia)',
'G4264': 'a business (pragmateuomai)',
'G4265': 'to do business (pragmatos)',
'G4266': 'a matter (praitorion)',
'G4267': 'the praetorium (praktor)',
'G4268': 'an officer (praxis)',
'G4269': 'a deed, practice (praios)',
'G4270': 'gentle (praotes)',
'G4271': 'gentleness (praotes)',
'G4272': '(gentleness (prais)',
'G4273': 'a plant (prasia)',
'G4274': 'a garden bed (prasso)',
'G4275': '(to do, practice (praus)',
'G4276': 'gentle (prautes)',
'G4277': 'gentleness (prepo)',
'G4278': 'to be fitting (presbeia)',
'G4279': 'an embassy (presbeuo)',
'G4280': 'to be an ambassador (presbuterion)',
'G4281': 'a council of elders (presbuteros)',
'G4282': 'an elder (presbutes)',
'G4283': 'an old man (presbutis)',
'G4284': 'an old woman (prenes)',
'G4285': 'forward, headlong (prion)',
'G4286': 'a saw (prizo)',
'G4287': 'to saw apart (prin)',
'G4288': '(before (Priska)',
'G4289': 'Prisca (Priskilla)',
'G4290':'(Priscilla (pro)',
'G4291': 'before (proago)',
'G4292': 'to lead before (proaireomai)',
'G4293': 'to choose before (proaitiaomai)',
'G4294': 'to accuse beforehand (proakouo)',
'G4295': 'to hear beforehand (proamartano)',
'G4296': 'to sin before (proaulion)',
'G4297': 'a gateway (probaino)',
'G4298': 'to go forward (proballo)',
'G4299': 'to put forward (probatikos)',
'G4300': 'of sheep (probaton)',
'G4301': 'a sheep (probibazo)',
'G4302': 'to urge forward (problepo)',
'G4303': '(to foresee (procheirizo)',
'G4304': 'to appoint (procheirotoneo)',
'G4305': 'to choose beforehand (progignosko)',
'G4306': 'to know beforehand (proginomai)',
'G4307': 'to happen before (prognosis)',
'G4308': 'foreknowledge (progonos)',
'G4309': 'a progenitor, parent (prographo)',
'G4310': 'to write before (prodelos)',
'G4311': 'evident beforehand (prodidomi)',
'G4311': '(to give before, betray (prodotes)',
'G4313': 'a betrayer (prodromos)',
'G4314': 'a forerunner (proeido)',
'G4315': 'to see beforehand (proelpizo)',
'G4316': 'to hope before (proeomai)',
'G4317':'(to say before (proereo)',
'G4318': 'to say before (proerchomai)',
'G4319': 'to go before (proetoimazo)',
'G4320': 'to prepare beforehand (proeuaggelizomai)',
'G4321': 'to preach the gospel beforehand (proechomai)',
'G4322': 'to have an advantage (proegeomai)',
'G4323': 'to go before (prothesis)',
'G4324': 'a setting forth, purpose (prothesmia)',
'G4325': 'an appointed time (prothumos)',
'G4326': 'ready, willing (prothumos)',
'G4327': '(readily (prothumia)',
'G4328': 'readiness, eagerness (proistemi)',
'G4329': 'to rule, manage (prokaleomai)',
'G4330': 'Same (to call forth, provoke (prokataggello)',
'G4331': 'to announce beforehand (prokatartizo)',
'G4332': 'to make ready beforehand (prokataleipo)',
'G4333': 'to leave behind (prokatalambano)',
'G4334': 'to take before (prokataskeuazo)',
'G4335': 'to prepare beforehand (prokeimai)',
'G4336': 'to be set before (prokerusso)',
'G4337': 'to preach beforehand (prokoima)',
'G4338': 'a suburb (prokope)',
'G4339': 'progress (prokopto)',
'G4340': 'to advance, proceed (prokrima)',
'G4341': 'prejudice (prokuroo)',
'G4342': 'to confirm beforehand (prolambano)',
'G4343': '(to take beforehand (prolego)',
'G4344': 'to say beforehand (proloma)',
'G4345': 'a forelock (promarturomai)',
'G4346': 'to testify beforehand (promeletao)',
'G4347': 'to premeditate (promerimnao)',
'G4348': 'to be anxious beforehand (pronoia)',
'G4349': 'forethought, providence (pronoeo)',
'G4350': 'to provide for (proorizo)',
'G4351': 'to predestine (proorao)',
'G4352': 'to see beforehand (propascho)',
'G4353': 'to suffer before (propempo)',
'G4354': '(to send forward (propetes)',
'G4355': 'reckless (prophero)',
'G4356': 'to bring forth (prophemi)',
'G4357': 'to speak beforehand (propheteia)',
'G4358': 'prophecy (propheteuo)',
'G4359': 'to prophesy (prophetes)',
'G4360': 'a prophet (prophetikos)',
'G4361': 'prophetic (prophetis)',
'G4362': 'a prophetess (prophthano)',
'G4363': 'to anticipate (procheiroo)',
'G4364': 'to deliver (procheiroo)',
'G4365': '(to deliver (proschomai)',
'G4366': 'to choose (Pros)',
'G4367': 'to, towards (pros)',
'G4368': 'to, towards (pro)',
'G4369': 'before (proago)',
'G4370': 'to lead before (proanabaino)',
'G4371': 'to go up before (proanaggello)',
'G4372': 'to announce beforehand (proanameno)',
'G4373': 'to wait for (proanapauomai)',
'G4374': 'to rest before (proapeimi)',
'G4375': 'to go away before (proapelpizo)',
'G4376': '(to hope before (proapostello)',
'G4377': 'to send before (prosarmozo)',
'G4378': 'to fit together (prosbaton)',
'G4379': 'a sheep (prosbaino)',
'G4380': 'to go to (prosballo)',
'G4381': 'to cast to (prosbibazo)',
'G4382': 'to bring to (prosblepo)',
'G4383': 'to look at (prosbrosis)',
'G4384': 'food (prosdapanao)',
'G4385': 'to spend in addition (prosdeomai)',
'G4386': '(to need besides (prosdechomai)',
'G4387': 'to receive, wait for (prosdechomai)',
'G4388': 'to receive (prosdokia)',
'G4389': 'expectation (proseao)',
'G4390': 'to permit further (proseggizo)',
'G4391': 'to approach (prosedreuo)',
'G4392': 'to attend to (proseleuomai)',
'G4393': 'to come to (proserchomai)',
'G4394': 'to come to, approach (proseuchomai)',
'G4395': 'to pray (proseuche)',
'G4396': 'prayer (prosecho)',
'G4397': '(to pay attention to (prosemeo)',
'G4398': 'to be near (prosena)',
'G4399': 'near (prosenegko)',
'G4400': 'to bring to (prosenegko)',
'G4401': 'to bring to (prosenegko)',
'G4402': 'to bring to (prosenegko)',
'G4403': 'to bring to (prosenegko)',
'G4404': 'to bring to (prosphero)',
'G4405': 'to bring to (prosphero)',
'G4406': 'an offering (prosphora)',
'G4407': 'acceptable (prosphiles)',
'G4408': 'a calling (prosphonesis)',
'G4409': 'to call to (prosphoneo)',
'G4410': 'a sound (proschusis)',
'G4411': 'a pouring upon (proschomai)',
'G4412': 'to be cold (prosops)',
'G4413': 'the face (prosopolepteo)',
'G4414': 'to show partiality (prosopoleptes)',
'G4415': 'a respecter of persons (prosopolepsia)',
'G4416': 'partiality (prospoiesis)',
'G4417': 'a feigning (prosporeuomai)',
'G4418': 'to come to (prosprosdechomai)',
'G4419': 'to receive (prosproskaleomai)',
'G4420': 'to call to (prosproskartereo)',
'G4421': 'to attend to (prosproskarteresis)',
'G4422': 'perseverance (prosproskephalaion)',
'G4423': 'a pillow (prosproskleroo)',
'G4424': 'to allot to (prosprosklino)',
'G4425': 'to incline to (prosprosklisis)',
'G4426': 'partiality (prosproskollao)',
'G4427': 'to join (prosproskope)',
'G4428': 'an offense (prosproskopto)',
'G4429': 'to strike against (prosproskuliomai)',
'G4430': 'to roll to (proskuneo)',
'G4431': 'to worship (proskunetes)',
'G4432': 'a worshiper (proslaleo)',
'G4433': 'to speak to (proslambano)',
'G4434': 'to take to (proslepsis)',
'G4435': 'an accepting (prosmeno)',
'G4436': 'to remain with (prosormizo)',
'G4437': 'to anchor at (prosochthizo)',
'G4438': 'to be angry with (prospeinao)',
'G4439': 'to be hungry (prosphagion)',
'G4440': 'food (prosphatos)',
'G4441': 'newly slain (prosphatos)',
'G4442': 'recently (prosphereia)',
'G4443': 'an offering (prosphero)',
'G4444': 'to bring to (prosphiles)',
'G4445': 'pleasing, agreeable (prosphora)',
'G4446': 'an offering (prosphoneo)',
'G4447': 'to call to (proschusis)',
'G4448': 'a pouring (prospsauo)',
'G4449': 'to touch (prosdechomai)',
'G4450': 'to receive (prosdokao)',
'G4451': 'to expect (prosdokia)',
'G4452': 'expectation (proseao)',
'G4453': 'to permit (proseggizo)',
'G4454': 'to approach (prosedreuo)',
'G4455': 'to wait on (proserchomai)',
'G4456': 'to come to (proseuchomai)',
'G4457': 'to pray (proseuche)',
'G4458': 'prayer (prosecho)',
'G4459': 'to pay attention (prosomoiazo)',
'G4460': 'to be like (prosomologeo)',
'G4461': 'to confess (prosopon)',
'G4462': 'the face (prosopolepteo)',
'G4463': 'to show partiality (prosopoleptes)',
'G4464': 'a respecter of persons (prosopolepsia)',
'G4465': 'partiality (prosporeuomai)',
'G4466': 'to go to (prostrecho)',
'G4467': 'to run to (prossabaton)',
'G4468': 'the day before the Sabbath (prosphagion)',
'G4469': 'anything eaten with bread (prosphero)',
'G4470': 'to bring to (prosphiles)',
'G4471': 'acceptable (prosphora)',
'G4472': 'an offering (prosphoneo)',
'G4473': '(to call to (prosphronos)',
'G4474': 'cheerfully (prosodizo)',
'G4475': 'to approach (prosphallo)',
'G4476': 'to dash against (proskairos)',
'G4477': 'temporary (proskaleomai)',
'G4478': 'to call to (proskartereo)',
'G4479': 'to continue steadfastly (proskarteresis)',
'G4480': 'perseverance (proskephalaion)',
'G4481': 'a pillow (proskleroo)',
'G4482': 'to allot to (prosklisis)',
'G4483': 'partiality (proskollao)',
'G4484': 'to join to (proskope)',
'G4485': 'an offense (proskopto)',
'G4486': 'to stumble (proskuliomai)',
'G4487': 'to roll to (proskuneo)',
'G4488': 'to worship (proskunetes)',
'G4489': 'a worshiper (proslaleo)',
'G4490': 'to speak to (proslambano)',
'G4491': 'to take to (proslepsis)',
'G4492': 'an accepting (prosmeno)',
'G4493': 'to continue with (prosochthizo)',
'G4494': 'to be grieved with (prosopon)',
'G4495': 'the face (prosopolepteo)',
'G4496': 'to show partiality (prosopolepsia)',
'G4497': 'partiality (prosphatos)',
'G4498': 'newly slain (prosphero)',
'G4499': 'to bring to (prosphora)',
'G4500': 'an offering',
'G4501': 'to call to (prophoneo)',
'G4502': 'to run to (protrecho)',
'G4503': 'to urge (protrepomai)',
'G4504': 'to set forth (prohypakouo)',
'G4505': 'to obey (prohyparcho)',
'G4506': 'to exist before (procheirizo)',
'G4507': 'to appoint (procheirotoneo)',
'G4508': 'to choose beforehand (Prochoros)',
'G4509': 'Prochorus (procheo)',
'G4510': 'to pour out (proteino)',
'G4511': 'to stretch out (proteron)',
'G4512': 'before (proteros)',
'G4513': 'former (protithemai)',
'G4514': 'to set forth (protomai)',
'G4515': 'to fly (prototokia)',
'G4516': 'a birthright (prototokos)',
'G4517': 'firstborn (protrecho)',
'G4518': 'to run before (proyparcho)',
'G4519': 'to exist before (prophero)',
'G4520': 'to bring forth (prophemi)',
'G4521': 'to speak before (propheteia)',
'G4522': 'prophecy (propheteuo)',
'G4523': 'to prophesy (prophetes)',
'G4524': 'a prophet (prophetikos)',
'G4525': 'prophetic (prophetis)',
'G4526': 'a prophetess (prophthano)',
'G4Next': 'to anticipate (procheirizo)',
'G4528': 'to appoint (procheirotoneo)',
'G4529': 'to choose beforehand (procha)',
'G4530': 'a ships prow (prumna)',
'G4531': 'the stern (prora)',
'G4532': 'a prow (proi)',
'G4533': 'early (proia)',
'G4534': 'early (proimos)',
'G4535': 'early (proinos)',
'G4536': 'early (proorao)',
'G4537': 'to see before (prophago)',
'G4538': 'to eat before (prosphagion)',
'G4539': 'food (prosphiles)',
'G4540': 'acceptable (prosphora)',
'G4541': 'an offering (prosphoneo)',
'G4542': 'to call to (proschomai)',
'G4543': 'to be cold (pros)',
'G4544': 'to, towards (prosabbaton)',
'G4545': 'the day before the Sabbath (prosagoge)',
'G4546': 'access (prosago)',
'G4547': 'to bring to (prosaitis)',
'G4548': 'a beggar (prosaiteo)',
'G4549': 'to beg (prosanalisko)',
'G4550': 'to spend besides (prosanapleroo)',
'G4551': 'to fill up (prosanalomai)',
'G4552': 'to spend besides (prosanatithemi)',
'G4553': 'to consult (prosapheileomai)',
'G4554': 'to perish (prosapollumi)',
'G4555': 'to destroy (prosapeileo)',
'G4556': 'to threaten further (prosdapanao)',
'G4557': 'to spend more (prosdeomai)',
'G4558': 'to need besides (prosdechomai)',
'G4559': 'to receive (prosdokao)',
'G4560': 'to expect (prosdokia)',
'G4561': 'expectation (prosdromos)',
'G4562': 'running to (proseao)',
'G4563': 'to permit (proseggizo)',
'G4564': 'to approach (prosedreuo)',
'G4565': 'to wait on (proserchomai)',
'G4566': 'to come to (proseuchomai)',
'G4567': 'to pray (proseuche)',
'G4568': 'prayer (prosecho)',
'G4569': 'to pay attention (prosomoiazo)',
'G4570': 'to be like (prosomologeo)',
'G4571': 'to confess (prosopon)',
'G4572': 'the face (prosopolepteo)',
'G4573': 'to show partiality (prosopoleptes)',
'G4574': 'a respecter of persons (prosopolepsia)',
'G4575': 'partiality (prosporeuomai)',
'G4576': 'to go to (prostrecho)',
'G4577': 'to run to (prossabaton)',
'G4578': 'the day before the Sabbath (prosphagion)',
'G4579': 'anything eaten with bread (prosphatos)',
'G4580': 'newly slain (prosphero)',
'G4581': 'to bring to (prosphiles)',
'G4582': 'acceptable (prosphora)',
'G4583': 'an offering (prosphoneo)',
'G4584': 'to call to (prosphronos)',
'G4585': 'cheerfully (proschomai)',
'G4586': 'to be cold (prospsauo)',
'G4587': 'to touch (prostithemi)',
'G4588': 'to add (prostrecho)',
'G4589': 'to run to (prostithemi)',
'G4590': 'to add (prostasso)',
'G4591': 'to command (prostithemi)',
'G4592': 'to add (prosphero)',
'G4593': 'to bring to (prosphora)',
'G4594': 'an offering (prosphoneo)',
'G4595': 'to call to (proschomai)',
'G4596': 'to be cold (pros)',
'G4597': 'to, towards (prosopon)',
'G4598': 'the face (prosphatos)',
'G4599': 'newly slain (prosphero)',
'G4600': 'to bring to (prosphora)',
'G4601': 'an offering (prosphoneo)',
'G4602': 'to call to (proschomai)',
'G4603': 'to be cold (prophthano)',
'G4604': 'to anticipate (procheirizo)',
'G4605': 'to appoint (procheirotoneo)',
'G4706': '(to choose beforehand (Prochoros)',
'G4607': 'Prochorus (procheo)',
'G4608': 'to pour out (ptaio)',
'G4609': 'to stumble (pterna)',
'G4610': 'the heel (pternizo)',
'G4611': 'to strike with the heel (ptochaino)',
'G4612': 'to be a beggar (ptocheia)',
'G4613': 'poverty (ptocheuo)',
'G4614': 'to be poor (ptochos)',
'G4615': 'poor (ptoesis)',
'G4616': 'terror (ptoeo)',
'G4617': 'to terrify (ptoma)',
'G4618': 'a corpse (ptosis)',
'G4619': 'a fall (pturo)',
'G4620': 'to terrify (ptuon)',
'G4621': 'a winnowing shovel (ptusma)',
'G4622': 'spittle (ptusso)',
'G4623': 'to fold (ptuo)',
'G4624': 'to spit (pugme)',
'G4625': 'the fist (Pudes)',
'G4626': 'Pudens (pulax)',
'G4627': 'a guard (pule)',
'G4628': 'a gate (pulon)',
'G4629': '(a gateway (punthanomai)',
'G4630': 'to inquire (puretos)',
'G4631': 'a fever (pur)',
'G4632': 'fire (pura)',
'G4633': 'a fire (purgos)',
'G4634': 'a tower (puresso)',
'G4635': 'to have a fever (purinos)',
'G4636': 'fiery (puroo)',
'G4637': 'to set on fire (purrhazo)',
'G4638': 'to be fiery red (purrhos)',
'G4639': 'fiery red (purrhos)',
'G4640': 'fiery red (purosis)',
'G4641': 'a burning (pus)',
'G4642': 'pus (pos)',
'G4643': 'how? (poleo)',
'G4644': 'to sell (polos)',
'G4645': 'a colt (ponos)',
'G4646': 'pain (porosis)',
'G4647': 'hardness (poroo)',
'G4648': 'to harden (pos)',
'G4649': 'at all (posos)',
'G4650': 'how great (potamos)',
'G4651': 'a river (pote)',
'G4652': 'when? (poterion)',
'G4653': 'a cup (potizo)',
'G4654': 'to give to drink (potos)',
'G4655':' (a drinking bout (pou)',
'G4656': 'where? (pous)',
'G4657': 'a foot (pragmateia)',
'G4658': 'a business (pragmateuomai)',
'G4659': 'to do business (praitorion)',
'G4660': 'the praetorium (praktor)',
'G4661': 'an officer (praxis)',
'G4662': 'a deed (praos)',
'G4663': 'gentle (praotes)',
'G4664': 'gentleness (prautes)',
'G4665': 'gentleness (prasso)',
'G4666': 'to do (prepo)',
'G4667': 'to be fitting (presbeia)',
'G4668': 'an embassy (presbeuo)',
'G4669': '(to be an ambassador (presbuterion)',
'G4670': 'a council of elders (presbuteros)',
'G4671': 'an elder (presbutes)',
'G4672': 'an old man (presbutis)',
'G4673': 'an old woman (prenes)',
'G4674': 'headlong (prizo)',
'G4675': 'to saw (prin)',
'G4676': 'before (Priska)',
'G4677': 'Prisca (Priskilla)',
'G4678': 'Priscilla (pro)',
'G4679': 'before (proago)',
'G4680': 'to lead forth (proaireomai)',
'G4681': 'to choose (proaitiaomai)',
'G4682': 'to accuse beforehand (proakouo)',
'G4683': 'to hear before (proamartano)',
'G4684': 'to sin before (proaulion)',
'G4685': 'a courtyard (probaino)',
'G4686': 'to go forward (proballo)',
'G4687': 'to put forward (probatikos)',
'G4688': 'of sheep (probaton)',
'G4689': 'a sheep (probibazo)',
'G4690': 'to urge forward (problepo)',
'G4691': 'to foresee (proginomai)',
'G4692': 'to happen before (proginosko)',
'G4693': 'to know before (prognosis)',
'G4694': 'foreknowledge (progonos)',
'G4695': '(a progenitor (prographo)',
'G4696': 'to write before (prodelos)',
'G4697': 'evident (prodidomi)',
'G4698': 'to give before, betray (prodotes)',
'G4699': 'a betrayer (prodromos)',
'G4700': 'a forerunner',
'G4701': 'to compassionate (splagchnizomai)',
'G4702': 'intestines, affections (splagchnon)',
'G4703': 'a sponge (spoggos)',
'G4704': 'ashes (spodos)',
'G4Example': 'example (hypodeigma)',
'G4705': 'a sowing (spora)',
'G4706': 'seed (sporimos)',
'G4707': 'sown field, grainfield (sporimos)',
'G4708': 'a seed (sporos)',
'G4709': 'to be eager, hasten (spoudazo)',
'G4710': 'eagerness, diligence (spoude)',
'G4711': 'eagerly, diligently (spoudaios)',
'G4712': 'more eagerly (spoudaioteros)',
'G4713': 'very eagerly (spoudaioteros)',
'G4714': 'eagerly (spoudaios)',
'G4715': 'a basket (spyris)',
'G4716': 'a racecourse, stadium (stadion)',
'G4717': 'a measure of distance (stadion)',
'G4718': 'a standing, stability (stasis)',
'G4719': 'a dissension, insurrection (stasis)',
'G4720': 'Stachys, a Christian (Stachys)',
'G4721': 'a twoedged sword (stachys)',
'G4722': 'a weight, a coin (stater)',
'G4723': 'a cross (stauros)',
'G4724': 'to crucify (stauroo)',
'G4725': 'a currant, raisin (staphyle)',
'G4726': 'a roof (stege)',
'G4727': 'to cover, endure (stego)',
'G4728': 'narrow (steiros)',
'G4729': 'barren (steiros)',
'G4730': 'Stephanas, a Christian (Stephanas)',
'G4731': 'a crown (stephanos)',
'G4732': 'to crown (stephanoo)',
'G4733': 'Stephen, a Christian (Stephanos)',
'G4734': 'the breast (stethos)',
'G4735': 'to set, stand (steko)',
'G4736': 'a prop, support (sterigmos)',
'G4737': 'to establish, strengthen (sterizo)',
'G4738': 'firm, steadfast (stereos)',
'G4739': 'to make firm, strengthen (stereo)',
'G4740': 'firmness, steadfastness (stereoma)',
'G4741': 'deprivation (steresis)',
'G4742': 'a faultfinder (stemnites)',
'G4743': 'a mark, brand (stigma)',
'G4744': 'a moment (stigme)',
'G4745': 'to shine (stilbo)',
'G4746': 'a portico, colonnade (stoa)',
'G4Example': 'example (hypodeigma)',
'G4747': 'Stoic, a philosopher (Stoikos)',
'G4748': 'a robe (stole)',
'G4749': 'a mouth (stoma)',
'G4750': 'the stomach (stomachos)',
'G4751': 'a sharp edge (stomachos)',
'G4752': 'a band of soldiers (stratiotes)',
'G4753': 'to make war, serve as a soldier (strateuomai)',
'G4754': 'a campaign, warfare (strateia)',
'G4755': 'an army (strateuma)',
'G4756': 'a commander (strategos)',
'GExample': 'example (hypodeigma)',
'G4757': 'a soldier (stratiotes)',
'G4758': 'a soldier (stratiotes)',
'G4759': 'to turn (strebloo)',
'G4760': 'to turn (strepho)',
'G4761': 'to turn (strepho)',
'G4762': 'restlessness, wastefulness (streniao)',
'G4763': 'to live riotously (streniao)',
'G4764': 'riotous luxury (strenos)',
'G4765': 'a turban (strouthion)',
'G4766': 'a sparrow (strouthion)',
'G4767': 'to spread (stronnumi)',
'G4768': 'Sosthenes, a Christian (Sosthenes)',
'G4769': 'Sosipater, a Christian (Sosipatros)',
'G4770': 'Sothenes, a Corinthian (Sothenes)',
'G4771': 'you (sy)',
'G4772': 'to boil (sygkino)',
'G4773': 'related by birth (syggenes)',
'G4774': 'a relative (syggenes)',
'G4775': 'a female relative (syggeneia)',
'G4776': 'relationship, kindred (syggeneia)',
'G4777': 'pardon, allowance (syggnome)',
'G4778': 'to collect, gather (sygkleronomos)',
'G4779': 'to call together (sygkaleo)',
'G4780': 'to cover, conceal (sygkalypto)',
'G4781': 'to bend together (sygkampto)',
'G4782': 'a fellow prisoner (sygkathizo)',
'G4783': 'to seat with (sygkathizo)',
'G4784': 'to suffer hardship with (sygkakopatheo)',
'G4785': 'to suffer with (sygkakoucheo)',
'G4786': 'to rejoice with (sygchairo)',
'G4787': 'to pour together, confuse (sygcheo)',
'G4788': 'to use (sygchraomai)',
'G4789': 'confusion, tumult (sygchysis)',
'G4790': 'to live with (syzao)',
'G4791': 'to join together (syzeuxis)',
'G4792': 'to yoke together (syzeugnumi)',
'G4793': 'to seek together, dispute (syzeteo)',
'G4794': 'a disputer (syzetetes)',
'G4795': 'disputation, questioning (syzetesis)',
'G4796': 'a yoke fellow (syzygos)',
'G4797': 'Sycar, a city (Sykar)',
'G4798': 'a fig tree (syke)',
'G4799': 'a fig (sykon)',
'G4800': 'a sycamore tree (sykomorea)',
'G4801': 'to defraud, accuse falsely (sykophanteo)',
'G4802': 'false accusation (sykophantia)',
'G4803': 'to strip, plunder (sylagogeo)',
'G4804': 'to meet, confer (syllaleo)',
'G4805': 'to seize, catch, conceive (syllambano)',
'G4806': 'to collect, gather (syllego)',
'G4807': 'to reckon with (syllogizomai)',
'G4808': 'to grieve with (syllypeomai)',
'G4809': 'Sylvanus, a Christian (Sylouanos)',
'G4810': 'a captive (symbaino)',
'G4811': 'to come together, happen (symbaino)',
'G4812': 'to put together, debate (symballo)',
'G4813': 'to reign with (symbasileuo)',
'G4814': 'a fellow elder (sympresbyteros)',
'G4815': 'to go up with (symbaino)',
'G4816': 'to lead astray with (symbaino)',
'G4817': 'to advise, consult (symbouleuo)',
'G4818': 'counsel, advice (symboulion)',
'G4819': 'a counselor (symboulos)',
'G4820': 'Symeon, two Israelites (Symeon)',
'G4821': 'Symeon, an apostle (Symeon)',
'G4822': 'a fellow disciple (symmathetes)',
'G4823': 'a fellow soldier (symmorphos)',
'G4824': 'conformed to (symmorphos)',
'G4825': 'to conform to (symmorphoo)',
'G4826': 'to suffer with (sympascho)',
'G4827': 'to feel sympathy (sympathes)',
'G4828': 'to suffer with, sympathize (sympatheo)',
'Additional': 'additional (prostithemi)',
'G4829': 'sympathy (sympathia)',
'G4830': 'to go with (symparaginomai)',
'G4831': 'to remain with (symparameno)',
'G4832': 'to be present with (sympareimi)',
'G4833': 'to drink with (sympino)',
'G4834': 'to send with (sympempo)',
'G4835': 'to be with (symperilambano)',
'G4836': 'to complete, enclose (sympleroo)',
'G4837': 'to choke (sympnigo)',
'G4838': 'a fellow citizen (sympolites)',
'G4839': 'to go with (symporeuomai)',
'G4840': 'a drinking party, banquet (symposion)',
'G4841': 'a company (symposion)',
'G4842': 'a fellow elder (sympresbyteros)',
'G4843': 'to agree with (symphoneo)',
'G4844': 'agreement (symphonesis)',
'G4845': 'agreement (symphonia)',
'G4846': 'harmonious (symphonos)',
'G4847': 'to vote with (symphyletos)',
'G4848': 'a fellow countryman (symphyletos)',
'G4849': 'to plant together (symphyo)',
'G4850': 'united with (symphytos)',
'G4851': 'to speak with (symphronizo)',
'G4852': 'to bring together, be profitable (symphero)',
'G4853': 'profitable, expedient (sympheron)',
'G4854': 'to vote against (symphora)',
'G4855': 'to rejoice with (synagoge)',
'G4856': 'a synagogue (synagoge)',
'G4857': 'to bring together, gather (synago)',
'G4858': 'to contend with (synagonizomai)',
'G4859': 'to exercise with (synathleo)',
'G4860': 'to assemble with (synathroizo)',
'G4861': 'to capture with (synaichmalotos)',
'G4862': 'a fellow captive (synaichmalotos)',
'G4863': 'to follow with (synakoloutheo)',
'G4864': 'to mix with (synalizo)',
'G4865': 'to depart with (synapago)',
'G4866': 'to perish with (synapothnesko)',
'G4867': 'to destroy with (synapollymi)',
'G4868': 'a fellow apostle (synapostolos)',
'G4869': 'to join closely (synarmolegeo)',
'G4870': 'to snatch away with (synarpazo)',
'G4871': 'to increase with (synauxano)',
'G4872': 'with (syn)',
'G4873': 'to go up with (synanabaino)',
'G4874': 'to recline with (synanakeimai)',
'G4875': 'to mix with (synanamignymi)',
'G4876': 'to lay hold with, help (synanapauomai)',
'G4877': 'to rest with (synanapauomai)',
'G4878': 'to meet with (synantao)',
'G4879': 'a meeting (synantesis)',
'G4880': 'to help with (synantilambanomai)',
'G4881': 'to speak against (synapago)',
'G4882': 'a fellow worker (synergos)',
'G4883': 'to work with (synergeo)',
'G4884': 'a fellow worker (synergos)',
'G4885': 'to go with (synerchomai)',
'G4886': 'to eat with (synesthio)',
'G4887': 'understanding (synesis)',
'G4888': 'intelligent (synetos)',
'G4889': 'to rejoice with (syneudokeo)',
'G4890': 'approval (syneudokia)',
'G4891': 'to know with, be conscious (syneido)',
'G4892': 'conscience (syneidesis)',
'G4893': 'to be with (syneimi)',
'G4894': 'to come together (syneimi)',
'G4895': 'to bring with (syneiserchomai)',
'G4896': 'a fellow traveler (synekdemos)',
'G4897': 'to choose with (syneklektos)',
'G4898': 'chosen with (syneklektos)',
'G4899': 'to send with (synepomai)',
'G4900': 'to follow with (synepomai)',
'G4901': 'to work together (synergeo)',
'G4902': 'a fellow worker (synergos)',
'G4903': 'to come together, meet (synerchomai)',
'G4904': 'to eat with (synesthio)',
'G4905': 'understanding (synesis)',
'G4906': 'intelligent (synetos)',
'G4907': 'to hold together, oppress (synecho)',
'G4908': 'to rejoice with (synedrion)',
'G4909': 'a council, the Sanhedrin (synedrion)',
'G4910': 'to know with, be conscious (syneido)',
'G4911': 'conscience (syneidesis)',
'G4912': 'to be with (syneimi)',
'G4913': 'to come together (syneimi)',
'G4914': 'to bring with (syneiserchomai)',
'G4915': 'a fellow traveler (synekdemos)',
'G4916': 'to choose with (syneklektos)',
'G4917': 'chosen with (syneklektos)',
'G4918': 'to send with (synepomai)',
'G4919': 'to follow with (synepomai)',
'G4920': 'to work together (synergeo)',
'G4921': 'a fellow worker (synergos)',
'G4922': 'to come together, meet (synerchomai)',
'G4923': 'to eat with (synesthio)',
'G4924': 'understanding (synesis)',
'G4925': 'intelligent (synetos)',
'G4926': 'to hold together, oppress (synecho)',
'G4927': 'a council, the Sanhedrin (synedrion)',
'G4928': 'to know with, be conscious (syneido)',
'G4929': 'conscience (syneidesis)',
'G4930': 'to be with (syneimi)',
'G4931': 'to come together (syneimi)',
'G4932': 'to bring with (syneiserchomai)',
'G4933': 'a fellow traveler (synekdemos)',
'G4934': 'to choose with (syneklektos)',
'G4935': 'chosen with (syneklektos)',
'G4936': 'to send with (synepomai)',
'G4937': 'to follow with (synepomai)',
'G4938': 'to work together (synergeo)',
'G4939': 'a fellow worker (synergos)',
'G4940': 'to come together, meet (synerchomai)',
'G4941': 'to eat with (synesthio)',
'G4942': 'understanding (synesis)',
'G4943': 'intelligent (synetos)',
'G4Example': 'example (hypodeigma)',
'G4944': 'to hold together, oppress (synecho)',
'G4945': 'to go with (synodia)',
'G4946': 'a company of travelers (synodia)',
'G4947': 'to dwell with (synoikeo)',
'G4948': 'to build with (synoikodomeo)',
'G4949': 'to talk with (synomileo)',
'G4950': 'bordering on (synomoreo)',
'G4951': 'to travel with (synodeuo)',
'Example': 'example (hypodeigma)',
'G4952': 'to know (synoida)',
'G4953': 'boundary, border (synoria)',
'G4954': 'to set together (synistao)',
'G4955': 'to recommend, stand with (synistemi)',
'G4956': 'to journey with (synodeuo)',
'G4957': 'a company of travelers (synodia)',
'G4958': 'to dwell with (synoikeo)',
'G4959': 'to build with (synoikodomeo)',
'G4960': 'to talk with (synomileo)',
'G4961': 'bordering on (synomoreo)',
'G4962': 'to travel with (synodeuo)',
'G4963': 'to know (synoida)',
'G4964': 'boundary, border (synoria)',
'G4Testing': 'testing (peirasmos)',
'G4965': 'to set together (synistao)',
'G4966': 'to recommend, stand with (synistemi)',
'G4967': 'to crucify with (synstauroo)',
'G4968': 'a fellow soldier (synstratiotes)',
'G4969': 'to form together (syschematizo)',
'G4970': 'dark-colored (synzotikos)',
'G4971': 'to raise with (synegeiro)',
'G4972': 'to seek with (synzeteo)',
'G4973': 'a disputer (synzetetes)',
'G4974': 'disputation (synzetesis)',
'G4975': 'to live with (syzao)',
'G4976': 'to yoke together (syzeuxis)',
'G4977': 'a yoke fellow (syzygos)',
'G4978': 'to join together (syzeugnumi)',
'G4979': 'Syracuse, a city (Syrakousai)',
'G4980': 'Syria (Syria)',
'G4981': 'a Syrian (Syros)',
'G4982': 'Syrophoenician (Syrophoinissa)',
'G4983': 'Syrtis, a sandbar (Syrtis)',
'G4984': 'to drag (syro)',
'G4985': 'Sychar, a city (Sychar)',
'G4986': 'Sychem, a city and a person (Sychem)',
'G4987': 'to form together (syschematizo)',
'G4988': 'nourishment (sitos)',
'G4989': 'a company (syssition)',
'G4990': 'to shake together (sysseio)',
'G4991': 'a sign, signal (syssemon)',
'G4992': 'a companion (syssomos)',
'G4993': 'of the same body (syssomos)',
'G4994': 'to rejoice with (synchairo)',
'G4995': 'to bewail, lament (systenazo)',
'G4996': 'to correspond to (systoicheo)',
'G4997': 'a fellow soldier (systratiotes)',
'G4998': 'to turn together, gather (systrepho)',
'G4999': 'a conspiracy, riot (systrophe)',
'G5000': 'to crucify with (systauroo)',
'G5001': 'Tabitha, a Christian woman (Tabitha)',
'G5002': 'a table (taberna)',
'G5003': 'a tent, tabernacle (tagma)',
'G5004': 'an order, rank (tagma)',
'G5005': 'to arrange, appoint (tasso)',
'G5006': 'orderly (taktos)',
'G5007': 'a talent (a weight and coin) (talanton)',
'G5008': 'a young girl (talitha)',
'G5009': 'Tamar, a woman (Tamar)',
'G5010': 'a storehouse, treasury (tameion)',
'G5011': 'so great, so large (tan)',
'G5012': 'to stretch (tan)',
'G5013': 'Tarsus, a city (Tarsos)',
'G5014': 'a Tarsian (Tarseus)',
'G5015': 'Tartarus, a place of punishment (Tartaroo)',
'G5Example': 'example (hypodeigma)',
'G5016': 'to place, set (tasso)',
'G5017': 'Tatian, a heretic (Tatianos)',
'G5018': 'this (tauta)',
'G5019': 'these (tauta)',
'G5020': 'the same (tauta)',
'G5021': 'to stretch (tasso)',
'G5022': 'Taurus, a mountain range (Tauros)',
'G5023': 'a grave, tomb (taphos)',
'G5024': 'burial (taphe)',
'G5025': 'to bury (thapto)',
'G5026': 'a lowly (tapeinos)',
'G5027': 'lowliness, humility (tapeinophrosyne)',
'G5028': 'to humble (tapeinoo)',
'G5029': 'humiliation, low estate (tapeinosis)',
'G5Example': 'example (hypodeigma)',
'G5030': 'quickly (tacheos)',
'G5031': 'more quickly (tachion)',
'G5032': 'most quickly (tachista)',
'G5033': 'quick, swift (tachys)',
'G5034': 'quickness, speed (tachos)',
'G5035': 'quickly, shortly (tacheos)',
'G5036': 'quick, swift (tachys)',
'G5037': 'a child (te)',
'G5038': 'both...and (te)',
'G5039': 'a wall (teichos)',
'G5040': 'a work of art (teichos)',
'G5Example': 'example (hypodeigma)',
'G5041': 'a child (teknion)',
'G5042': 'to bear children (teknogoneo)',
'G5043': 'childbearing (teknogonia)',
'G5044': 'a child (teknon)',
'G5045': 'to beget children (teknotropheo)',
'G5046': 'to bring up children (teknotropheo)',
'G5047': 'a carpenter (tekton)',
'G5048': 'Tertius, a Christian (Tertios)',
'G5049': 'Tertullus, an orator (Tertullos)',
'G5Example': 'example (hypodeigma)',
'G5050': 'a proof, sign (tekmerion)',
'G5051': 'an end, limit (telos)',
'G5052': 'to bring to an end, complete (teleioo)',
'G5053': 'completion, perfection (teleiosis)',
'G5054': 'a completer, perfecter (teleiotes)',
'G5055': 'to finish, complete (teleo)',
'G5056': 'perfect, complete (teleios)',
'G5057': 'perfectly (teleios)',
'G5058': 'perfection (teleiotes)',
'G5059': 'to bring to an end (teleo)',
'G5060': 'to finish (teleo)',
'G5061': 'an end, tax, custom (telos)',
'G5062': 'a tax collector (telones)',
'G5063': 'a tax office (telonion)',
'G5064': 'a monster, prodigy (teras)',
'G5065': 'Teresh, a eunuch (Teres)',
'G5066': 'to rub (tribo)',
'G5067': 'to watch, keep (tereo)',
'G5068': 'a keeping, observance (teresis)',
'G5069': 'Thaddaeus, an apostle (Thaddaios)',
'G5070': 'Thahash, a person (Thachas)',
'G5071': 'Thara, father of Abraham (Thara)',
'G5072': 'to be bold, confident (tharrheo)',
'G5073': 'to be bold (tharrheo)',
'G5074': 'courage, confidence (tharsos)',
'G5075': 'to be of good courage (tharseo)',
'G5076': 'a wonder, marvel (thauma)',
'G5Example': 'example (hypodeigma)',
'G5077': 'wonderful, marvelous (thaumastos)',
'G5078': 'to wonder, marvel (thaumazo)',
'G5079': 'Thebes, a city (Thebai)',
'G5080': 'Thebez, a place (Thebes)',
'G5081': 'a goddess (thea)',
'G5082': 'to see, behold (theaomai)',
'G5083': 'a theater (theatron)',
'G5Example': 'example (hypodeigma)',
'G5084': 'to make a spectacle of (theatrizo)',
'G5085': 'a sword (thele)',
'G5086': 'Theophilus, a person (Theophilos)',
'G5087': 'to will, wish (thelo)',
'G5088': 'a will, wish (thelema)',
'G5089': 'a will (thelesis)',
'G5090': 'Thessalonica, a city (Thessalonike)',
'G5091': 'a Thessalonian (Thessalonikeus)',
'G5092': 'Theudas, an insurgent (Theudas)',
'G5093': 'to see, behold (theoreo)',
'G5094': 'a spectator (theoros)',
'G5095': 'a sight, spectacle (theoria)',
'G5096': 'a case, sheath (theke)',
'G5097': 'to suckle (thelazo)',
'G5098': 'female (thelys)',
'G5099': 'a foundation (themelios)',
'G5100': 'to lay a foundation (themelioo)',
'G5101': 'a foundation (themelion)',
'G5102': 'God (theos)',
'G5103': 'divine (theios)',
'G5104': 'divinity, godhead (theiotes)',
'G5105': 'sulfur, brimstone (theion)',
'G5106': 'divine (theios)',
'G5107': 'God-breathed, inspired (theopneustos)',
'G5108': 'to fight against God (theomacheo)',
'G5109': 'a fighter against God (theomachos)',
'G5110': 'godlessness (theosebeia)',
'G5111': 'godly, devout (theosebes)',
'G5112': 'godliness (theosebeia)',
'G5113': 'a hater of God (theostyges)',
'G5114': 'Godhead, divinity (theotes)',
'G5115': 'to serve, heal (therapeuo)',
'G5116': 'healing, service (therapeia)',
'G5117': 'a servant, attendant (therapon)',
'G5118': 'to reap, harvest (therizo)',
'G5119': 'a harvest (therismos)',
'G5120': 'a reaper (theristes)',
'G5121': 'heat (therme)',
'G5122': 'to heat (thermaino)',
'G5123': 'summer (theros)',
'G5124': 'a storehouse (thesauros)',
'G5125': 'to store up, treasure (thesaurizo)',
'G5126': 'to bruise (thlao)',
'G5127': 'pressure, affliction (thlipsis)',
'G5128': 'to press, afflict (thlibo)',
'G5129': 'to die (thnesko)',
'G5130': 'mortal (thnetos)',
'G5Example': 'example (hypodeigma)',
'G5131': 'to make a noise, roar (thorbeo)',
'G5132': 'a noise, tumult (thorybos)',
'G5133': 'a fragment (thrausma)',
'G5134': 'to break in pieces (thrauo)',
'G5135': 'a lamb (thremma)',
'G5136': 'a footstool (threnos)',
'G5137': 'to wail, lament (threneo)',
'G5138': 'a lamentation (threnos)',
'G5139': 'religion, worship (threskeia)',
'G5140': 'religious, devout (threskos)',
'G5141': 'a throne (thronos)',
'G5142': 'Thyatira, a city (Thyatira)',
'G5143': 'a daughter (thygater)',
'G5144': 'a little daughter (thygatrion)',
'G5145': 'thyine wood (thyinos)',
'G5146': 'a storm, tempest (thyella)',
'G5147': 'incense (thymiama)',
'G5148': 'a censer (thymiaterion)',
'G5149': 'to burn incense (thymiao)',
'G5150': 'to be angry (thymomacheo)',
'G5151': 'passion, anger (thymos)',
'G5152': 'to be angry (thymoo)',
'G5153': 'a door (thyra)',
'G5154': 'a doorkeeper, porter (thyroros)',
'G5155': 'a large shield (thyreos)',
'G5156': 'a window (thyris)',
'G5157': 'a sacrifice (thysia)',
'G5158': 'an altar (thysiasterion)',
'G5159': 'to sacrifice (thyo)',
'G5160': 'Thomas, an apostle (Thomas)',
'G5161': 'a breastplate (thorax)',
'G5162': 'Tiberias, a city and lake (Tiberias)',
'G5163': 'Tiberius, a Roman emperor (Tiberios)',
'G5164': 'to put, place (tithemi)',
'G5165': 'Timaeus, a person (Timaios)',
'G5166': 'to honor, value (timao)',
'G5167': 'honor, price, value (time)',
'G5168': 'precious, honored (timios)',
'G5169': 'preciousness, costliness (timiotes)',
'G5170': 'Timon, a Christian (Timon)',
'G5171': 'Timothy, a Christian (Timotheos)',
'G5172': 'to punish (timoreo)',
'G5Example': 'example (hypodeigma)',
'G5173': 'punishment (timoria)',
'G5174': 'to suffer, experience (tino)',
'G5175': 'who, which, what (tis)',
'G5176': 'someone, anyone (tis)',
'G5177': 'Titan, a mythological figure (Titan)',
'G5178': 'Titus, a Christian (Titos)',
'G5179': 'Titius, a Christian (Titos)',
'G5180': 'to pay (tino)',
'G5181': 'to this (toi)',
'G5182': 'of this (toi)',
'G5183': 'such (toioutos)',
'G5184': 'therefore (toigaroun)',
'G5185': 'truly, indeed (toinyn)',
'G5PLAY': 'to play (paizo)',
'G5186': 'a wall (toichos)',
'G5187': 'a τόκος, interest (tokos)',
'G5188': 'to dare (tolmao)',
'G5189': 'more boldly (tolmeroteros)',
'G5190': 'boldness, daring (tolmetes)',
'G5191': 'sharper (tomoteros)',
'G5192': 'so great, so much (tosoutos)',
'G5193': 'then (tote)',
'G5194': 'of this (toutou)',
'G5195': 'this (touto)',
'G5196': 'a bow (toxon)',
'G5197': 'a table (trapeza)',
'G5198': 'a banker (trapezites)',
'G5199': 'a wound (trauma)',
'G5200': 'to wound (traumatizo)',
}
































































# ------------------------
# Cipher definitions (Unchanged)
# ------------------------
def keep_letters_upper(s: str) -> str:
    if not s: return ""
    normalized = unicodedata.normalize("NFKD", s)
    ascii_only = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return re.sub(r"[^A-Z]", "", ascii_only.upper())
































































def sum_map(s: str, m: dict) -> int:
    return sum(m.get(ch, 0) for ch in s)
































































A2Z = {chr(65+i): i+1 for i in range(26)}
REDUCTION = {chr(65+i): (i % 9) + 1 for i in range(26)}
REV_ORD = {chr(65+i): 26-i for i in range(26)}
CHALDEAN = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':8,'G':3,'H':5,'I':1,'J':1,'K':2,
            'L':3,'M':4,'N':5,'O':7,'P':8,'Q':1,'R':2,'S':3,'T':4,'U':6,'V':6,
            'W':6,'X':5,'Y':1,'Z':7}
JEWISH = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':600,'K':10,'L':20,
           'M':30,'N':40,'O':50,'P':60,'Q':70,'R':80,'S':90,'T':100,'U':200,'V':700,
           'W':900,'X':300,'Y':400,'Z':500}
































































def alw_kabbalah(s: str) -> int:
    t = 0
    for i, ch in enumerate(s):
        base = (ord(ch) - 64)
        val = ((base + i) % 26) or 26
        t += val
    return t
































































CIPHERS = [
    ("English Ordinal", lambda s: sum_map(s, A2Z)),
    ("Simple Gematria", lambda s: sum_map(s, REDUCTION)),
    ("Reverse Ordinal", lambda s: sum_map(s, REV_ORD)),
    ("Chaldean", lambda s: sum_map(s, CHALDEAN)),
    ("Jewish Gematria", lambda s: sum_map(s, JEWISH)),
    ("ALW Kabbalah", alw_kabbalah),
]
for i in range(1, 26):
    CIPHERS.append((f"Caesar Shift +{i}", lambda s, k=i: sum((((ord(ch)-65+k) % 26) + 1) for ch in s)))
for i in range(2, 51):
    CIPHERS.append((f"Ordinal x{i}", lambda s, k=i: sum_map(s, A2Z) * k))
for i in range(2, 22):
    CIPHERS.append((f"Reverse Ordinal x{i}", lambda s, k=i: sum_map(s, REV_ORD) * k))
assert len(CIPHERS) == 100
































































# ------------------------
# Bible & Quran structures (Unchanged)
# ------------------------
BIBLE_STRUCTURE = OrderedDict([
    ("Genesis", [31,25,24,26,32,22,24,22,29,32,32,20,18,24,21,16,27,33,38,18,34,24,20,67,34,35,46,22,35,43,55,32,20,31,29,43,36,30,23,23,57,38,34,34,28,34,31,22,33,26]), ("Exodus", [22,25,22,31,23,30,25,32,35,29,10,51,22,31,27,36,16,27,25,26,36,31,33,18,40,37,21,43,46,38,18,35,23,35,35,38,29,31,43,38]), ("Leviticus", [17,16,17,35,19,30,38,36,24,20,47,8,59,57,33,34,16,30,37,27,24,33,44,23,55,46,34]), ("Numbers", [54,34,51,49,31,27,89,26,23,36,35,16,33,45,41,50,13,32,22,29,35,41,30,25,18,65,23,31,40,16,54,42,56,29,34,13]), ("Deuteronomy", [46,37,29,49,33,25,26,20,29,22,32,32,18,29,23,22,20,22,21,20,23,30,25,22,19,19,26,68,29,20,30,52,29,12]), ("Joshua", [18,24,17,24,15,27,26,35,27,43,23,24,33,15,63,10,18,28,51,9,45,34,16,33]), ("Judges", [36,23,31,24,31,40,25,35,57,18,40,15,25,20,20,31,13,31,30,48,25]), ("Ruth", [22,23,18,22]), ("1 Samuel", [28,36,21,22,12,21,17,22,27,27,15,25,23,52,35,23,58,30,24,42,15,23,29,22,44,25,12,25,11,31,13]), ("2 Samuel", [27,32,39,12,25,23,29,18,13,19,27,31,39,33,37,23,29,33,43,26,22,51,39,25]), ("1 Kings", [53,46,28,34,18,38,51,66,28,29,43,33,34,31,21,34,24,46,21,43,29,53]), ("2 Kings", [18,25,27,44,27,33,20,29,37,36,20,21,25,29,38,20,41,37,37,20,21,26,20,37,20,30]), ("1 Chronicles", [54,55,24,43,26,81,40,40,44,14,47,40,14,17,29,43,27,17,19,8,30,19,32,31,31,32,34,21,30]), ("2 Chronicles", [17,18,17,22,14,42,22,18,31,19,23,16,22,15,19,14,19,34,11,37,20,12,21,27,28,23,9,27,36,27,21,33,25,33,27,23]), ("Ezra", [11,70,13,24,17,22,28,36,15,44]), ("Nehemiah", [11,20,32,23,19,19,73,18,38,39,36,47,31]), ("Esther", [22,23,15,17,14,14,10,17,32,3]), ("Job", [22,13,26,21,27,30,21,22,35,22,20,25,28,22,35,22,16,21,29,29,34,30,17,25,6,14,23,28,25,31,40,22,33,37,16,33,24,41,30,24,34,17]), ("Psalms", [6,12,8,8,12,10,17,9,20,18,7,8,6,7,5,11,15,50,14,9,13,31,6,10,22,12,14,9,11,12,24,11,22,22,28,12,40,22,13,17,13,11,5,26,17,11,9,14,20,23,19,9,6,7,23,13,11,11,17,12,8,12,11,10,13,20,7,35,36,5,24,20,28,23,10,12,20,72,13,19,16,8,18,12,13,17,7,18,52,17,16,15,5,23,11,13,12,9,9,5,8,28,22,35,45,48,43,13,31,7,10,10,9,8,18,19,2,29,176,7,8,9,4,8,5,6,5,6,8,8,3,18,3,3,21,7,7,11,8,8,12,4,5,6,7,15,20,10,9,11,6]), ("Proverbs", [33,16,35,27,23,35,27,36,18,32,31,28,25,35,33,33,28,24,29,30,31,29,35,34,28,28,27,28,27,33,31]), ("Ecclesiastes", [18,26,22,16,20,12,29,17,18,20,10,14]), ("Song of Solomon", [17,17,11,16,16,13,13,14]), ("Isaiah", [31,22,26,6,30,13,25,22,21,34,16,6,22,32,9,14,14,7,25,6,17,25,18,23,12,21,13,29,24,33,9,20,24,17,10,22,38,22,8,31,29,25,28,28,5,13,15,22,26,11,23,15,12,17,13,12,21,14,21,22,11,12,19,25,24,24]), ("Jeremiah", [19,37,25,31,31,30,34,22,26,25,23,17,27,22,21,21,27,23,15,18,14,30,40,10,38,24,22,17,32,24,40,44,26,22,19,32,21,28,18,16,18,22,13,30,5,28,7,47,39,46,64,34]), ("Lamentations", [22,22,66,22,22]), ("Ezekiel", [28,10,27,17,17,14,27,18,17,22,25,28,23,23,8,63,24,32,14,49,32,31,49,27,17,21,36,26,21,26,18,32,33,31,15,38,28,23,29,49,26,20,27,31,25,24,23,35]), ("Daniel", [21,49,30,37,31,28,28,27,27,21,45,13]), ("Hosea", [11,23,5,19,15,11,16,14,17,15,12,14,16,9]), ("Joel", [20,32,21]), ("Amos", [15,16,15,13,27,14,17,14,15]), ("Obadiah", [21]), ("Jonah", [17,10,10,11]), ("Micah", [16,13,12,13,15,16,20]), ("Nahum", [15,13,19]), ("Habakkuk", [17,20,19]), ("Zephaniah", [18,15,20]), ("Haggai", [15,23]), ("Zechariah", [21,13,10,14,11,15,14,23,17,12,17,14,9,21]), ("Malachi", [14,17,18,6]), ("Matthew", [25,23,17,25,48,34,29,34,38,42,30,50,58,36,39,28,27,35,30,34,46,46,39,51,46,75,66,20,1128]), ("Mark", [45,28,35,41,43,56,37,38,50,52,33,44,37,72,47,20]), ("Luke", [80,52,38,44,39,49,50,56,62,42,54,59,35,35,32,31,37,43,48,47,38,71,56,53]), ("John", [51,29,36,54,47,71,53,59,41,42,57,50,38,31,27,33,26,40,42,31,25,316]), ("Acts", [26,47,26,37,42,15,60,40,43,48,30,25,52,28,41,40,34,28,41,38,40,30,35,27,27,32,44,31]), ("Romans", [32,29,31,25,21,23,25,39,33,21,36,21,14,23,33,27]), ("1 Corinthians", [31,16,23,21,13,20,40,13,27,33,34,31,13,40,58,24]), ("2 Corinthians", [24,17,18,18,21,18,16,24,15,18,33,21,14]), ("Galatians", [24,21,29,31,26,18]), ("Ephesians", [23,22,21,32,33,24]), ("Philippians", [30,30,21,23]), ("Colossians", [29,23,25,18]), ("1 Thessalonians", [10,20,13,18,28]), ("2 Thessalonians", [12,17,18]), ("1 Timothy", [20,15,16,16,25,21]), ("2 Timothy", [18,26,17,22]), ("Titus", [16,15,15]), ("Philemon", [25]), ("Hebrews", [14,18,19,16,14,20,28,13,28,39,40,29,25]), ("James", [27,26,18,17,20]), ("1 Peter", [25,25,22,19,14]), ("2 Peter", [21,22,18]), ("1 John", [10,29,24,21,21,316]), ("2 John", [13]), ("3 John", [14,316]), ("Jude", [25]), ("Revelation", [20,29,22,11,14,17,17,13,21,11,19,17,18,20,8,21,18,24,21,15,27,21])
])
































































QURAN_STRUCTURE = {
    1: 7, 2: 286, 3: 200, 4: 176, 5: 120, 6: 165, 7: 206, 8: 75, 9: 129, 10: 109,
    11: 123, 12: 111, 13: 43, 14: 52, 15: 99, 16: 128, 17: 111, 18: 110, 19: 98, 20: 135,
    21: 112, 22: 78, 23: 118, 24: 64, 25: 77, 26: 227, 27: 93, 28: 88, 29: 69, 30: 60,
    31: 34, 32: 30, 33: 73, 34: 54, 35: 45, 36: 83, 37: 182, 38: 88, 39: 75, 40: 85,
    41: 54, 42: 53, 43: 89, 44: 59, 45: 37, 46: 35, 47: 38, 48: 29, 49: 18, 50: 45,
    51: 60, 52: 49, 53: 62, 54: 55, 55: 78, 56: 96, 57: 29, 58: 22, 59: 24, 60: 13,
    61: 14, 62: 11, 63: 11, 64: 18, 65: 12, 66: 12, 67: 30, 68: 52, 69: 52, 70: 44,
    71: 28, 72: 28, 73: 20, 74: 56, 75: 40, 76: 31, 77: 50, 78: 40, 79: 46, 80: 42,
    81: 29, 82: 19, 83: 36, 84: 25, 85: 22, 86: 17, 87: 19, 88: 26, 89: 30, 90: 20,
    91: 15, 92: 21, 93: 11, 94: 8, 95: 8, 96: 19, 97: 5, 98: 8, 99: 8, 100: 11,
    101: 11, 102: 8, 103: 3, 104: 9, 105: 5, 106: 4, 107: 7, 108: 3, 109: 6, 110: 3,
    111: 5, 112: 4, 113: 5, 114: 6
}
































































# ------------------------
# Builders & Loaders (Unchanged)
# ------------------------
def create_strongs_db() -> set:
    strongs_db = set()
    for i in range(1, 8675): strongs_db.add(f"H{i}")
    for i in range(1, 5625): strongs_db.add(f"G{i}")
    return strongs_db
































































def create_scripture_db() -> dict:
    scripture_db = {"chapters": defaultdict(set), "verses": defaultdict(set), "surahs": defaultdict(set), "ayahs": defaultdict(set)}
    book_abbr = [
        "Gen","Exo","Lev","Num","Deu","Jos","Jdg","Rut","1Sa","2Sa","1Ki","2Ki","1Ch","2Ch","Ezr","Neh","Est","Job","Psa","Pro",
        "Ecc","Sos","Isa","Jer","Lam","Eze","Dan","Hos","Joe","Amo","Oba","Jon","Mic","Nah","Hab","Zep","Hag","Zec","Mal","Mat",
        "Mar","Luk","Joh","Act","Rom","1Co","2Co","Gal","Eph","Php","Col","1Th","2Th","1Ti","2Ti","Tit","Phm","Heb","Jam","1Pe",
        "2Pe","1Jo","2Jo","3Jo","Jude","Rev"
    ]
    bi = 0
    for book_name, chapters in BIBLE_STRUCTURE.items():
        abbr = book_abbr[bi] if bi < len(book_abbr) else book_name[:3]
        for chap_num, verse_count in enumerate(chapters, 1):
            scripture_db["chapters"][chap_num].add(abbr)
            for verse_num in range(1, verse_count+1):
                scripture_db["verses"][verse_num].add(abbr)
        bi += 1
    for surah_num, ayah_count in QURAN_STRUCTURE.items():
        scripture_db["surahs"][surah_num].add(f"Q{surah_num}")
        for ayah_num in range(1, ayah_count+1):
            scripture_db["ayahs"][ayah_num].add(f"Q{surah_num}")
    return scripture_db
































































def load_strongs_from_excel(xlsx_path: str) -> dict:
    try:
        xls = pd.read_excel(xlsx_path, sheet_name=None, engine='openpyxl')
    except FileNotFoundError:
        print(f"Error: Strong's Excel file not found at {xlsx_path}")
        return {}
    except Exception as e:
        print(f"Could not load Strong's Excel: {e}")
        return {}
































































    mapping = {}
    print(f"Loading Strong's definitions from: {xlsx_path}")
    for name, df in xls.items():
        df.columns = [str(c).strip() for c in df.columns]
































































        num_col = None
        possible_num_cols = ['#', 'Strong', 'Strong\'s No', 'Number', 'No']
        for pnc in possible_num_cols:
            if pnc in df.columns: num_col = pnc; break
        if not num_col:
            for col in df.columns:
                 if any(k in col.lower() for k in ('#','strong','no','number')): num_col = col; break
        if not num_col: print(f"  Skipping sheet '{name}': Could not find number column."); continue
































































        text_col = None
        possible_text_cols = ['Gloss', 'Definition', 'Word', 'Lemma', 'Text', 'Meaning']
        for ptc in possible_text_cols:
            if ptc in df.columns: text_col = ptc; break
        if not text_col:
             for col in df.columns:
                 if any(k in col.lower() for k in ('gloss','definition','word','lemma','text','meaning')): text_col = col; break
        if not text_col:
            print(f"  Warning: Sheet '{name}' - No primary gloss column. Trying fallback.")
            num_col_index = df.columns.get_loc(num_col)
            for i in range(num_col_index + 1, len(df.columns)):
                col_name = df.columns[i]
                if pd.api.types.is_string_dtype(df[col_name]) or pd.api.types.is_object_dtype(df[col_name]):
                     if df[col_name].head().astype(str).str.strip().any():
                         text_col = col_name; print(f"  Using column '{text_col}' as fallback."); break
            if not text_col: print(f"  Skipping sheet '{name}': No suitable gloss column."); continue
































































        processed_count = 0
        for index, row in df.iterrows():
            raw_num = row[num_col]; raw_text = row.get(text_col)
            num = None
            try:
                if isinstance(raw_num, (float, int)):
                     if pd.notna(raw_num): num = int(raw_num)
                elif isinstance(raw_num, str):
                    digits = ''.join(ch for ch in raw_num if ch.isdigit());
                    if digits: num = int(digits)
            except ValueError:
                 digits = ''.join(ch for ch in str(raw_num) if ch.isdigit());
                 if digits:
                     try: num = int(digits)
                     except ValueError: pass
            if num is None: continue
































































            key = None
            if any(k in name.lower() for k in ['heb', 'ot']): key = f"H{num}"
            elif any(k in name.lower() for k in ['gre', 'gk', 'nt']): key = f"G{num}"
            else:
                if 1 <= num <= 8674: key = f"H{num}"
                elif 1 <= num <= 5624: key = f"G{num}"
                else: continue
































































            text = '';
            if pd.notna(raw_text) and isinstance(raw_text, str): text = raw_text.strip()
            elif pd.notna(raw_text): text = str(raw_text).strip()
            if not text:
                 for c in df.columns:
                     if c != num_col and c != text_col:
                         alt_val = row.get(c);
                         if pd.notna(alt_val):
                             alt_str = str(alt_val).strip();
                             if alt_str: text = alt_str; break
            mapping[key] = text; processed_count += 1
        print(f"  Processed {processed_count} entries from sheet '{name}'.")
    print(f"Finished loading Strong's definitions. Total loaded: {len(mapping)}")
    return mapping
































































# ------------------------
# Formatting & Matching Helpers (Unchanged)
# ------------------------
def find_scripture_by_split(number: int, bible_structure: dict = BIBLE_STRUCTURE):
    s = str(number)
    results = []
    # Iterate through possible split points
    for i in range(1, len(s)):
        try:
            # Assign chap and verse inside the try block
            chap = int(s[:i])
            verse = int(s[i:])
            # Basic sanity check, also inside the try block
            if chap <= 0 or verse <= 0:
                continue # Skip this split if numbers are invalid
        except ValueError:
            # This except catches errors from int() conversion
            continue # Skip if parts aren't integers
































































        # Check against Bible structure (This part is outside the try...except)
        for book, chaps in bible_structure.items():
            # Check if chapter number is valid for the book
            # and verse number is valid for that chapter
            if 1 <= chap <= len(chaps) and 1 <= verse <= chaps[chap-1]:
                results.append((book, chap, verse))
































































    if not results: return None
































































    # Prioritize certain books if multiple matches (e.g., Matthew often intended)
    priority_books = ["Matthew", "John", "Genesis", "Psalms", "Isaiah"]
    for book_name in priority_books:
        for r in results:
            if r[0] == book_name:
                return r # Return the first priority match found
































































    # If no priority match, return the first result found
    return results[0]
































































def format_strongs_and_scripture(value: int, strongs_map: dict):
    key_h, key_g = f"H{value}", f"G{value}"; strong_text, strong_key = None, None
    if key_h in strongs_map and strongs_map[key_h]: strong_key, strong_text = key_h, strongs_map[key_h]
    elif key_g in strongs_map and strongs_map[key_g]: strong_key, strong_text = key_g, strongs_map[key_g]
    elif key_h in BUILTIN_STRONGS: strong_key, strong_text = key_h, BUILTIN_STRONGS[key_h]
    elif key_g in BUILTIN_STRONGS: strong_key, strong_text = key_g, BUILTIN_STRONGS[key_g]
































































    if strong_key and strong_text:
        display_text = ' '.join(strong_text.split());
        if len(display_text) > 70: display_text = display_text[:67] + "...";
        middle = f'{strong_key} "{display_text}"'
    else:
        is_valid_h, is_valid_g = (1 <= value <= 8674), (1 <= value <= 5624);
        if is_valid_h and is_valid_g: middle = f'H{value} | G{value} "<no lookup>"'
        elif is_valid_h: middle = f'H{value} "<no lookup>"'
        elif is_valid_g: middle = f'G{value} "<no lookup>"'
        else: middle = f'{value} "<out of range>"'
































































    split = find_scripture_by_split(value);
    if split:
        book, chap, verse = split;
        book_abbr_map = {"Genesis": "Gen", "Exodus": "Exo", "Leviticus": "Lev", "Numbers": "Num", "Deuteronomy": "Deu", "Joshua": "Jos", "Judges": "Jud", "Ruth": "Rut", "1 Samuel": "1Sa", "2 Samuel": "2Sa", "1 Kings": "1Ki", "2 Kings": "2Ki", "1 Chronicles": "1Ch", "2 Chronicles": "2Ch", "Ezra": "Ezr", "Nehemiah": "Neh", "Esther": "Est", "Job": "Job", "Psalms": "Psa", "Proverbs": "Pro", "Ecclesiastes": "Ecc", "Song of Solomon": "Sos", "Isaiah": "Isa", "Jeremiah": "Jer", "Lamentations": "Lam", "Ezekiel": "Eze", "Daniel": "Dan", "Hosea": "Hos", "Joel": "Joe", "Amos": "Amo", "Obadiah": "Oba", "Jonah": "Jon", "Micah": "Mic", "Nahum": "Nah", "Habakkuk": "Hab", "Zephaniah": "Zep", "Haggai": "Hag", "Zechariah": "Zec", "Malachi": "Mal", "Matthew": "Mat", "Mark": "Mar", "Luke": "Luk", "John": "Joh", "Acts": "Act", "Romans": "Rom", "1 Corinthians": "1Co", "2 Corinthians": "2Co", "Galatians": "Gal", "Ephesians": "Eph", "Philippians": "Php", "Colossians": "Col", "1 Thessalonians": "1Th", "2 Thessalonians": "2Th", "1 Timothy": "1Ti", "2 Timothy": "2Ti", "Titus": "Tit", "Philemon": "Phm", "Hebrews": "Heb", "James": "Jam", "1 Peter": "1Pe", "2 Peter": "2Pe", "1 John": "1Jo", "2 John": "2Jo", "3 John": "3Jo", "Jude": "Jud", "Revelation": "Rev"};
        display_book = book_abbr_map.get(book, book[:3]);
        right = f'{display_book} {chap}:{verse}'
    else: right = '<no scripture split>'
    return f'{value:<5} > {middle:<80} > {right}'
































































def get_strongs_match(db: set, number: int) -> str:
    g_key, h_key = f'G{number}', f'H{number}'; g_match, h_match = g_key in db, h_key in db;
    if g_match and h_match: return f"{g_key} | {h_key}"
    elif g_match: return g_key
    elif h_match: return h_key
    else: return '---'
































































def get_scripture_match_compact(db: dict, number: int) -> str:
    parts = [];
    if number in db['chapters'] or number in db['verses']: parts.append(f'B:{number}')
    if number in db['surahs'] or number in db['ayahs']: parts.append(f'Q:{number}')
    return ' | '.join(parts) if parts else '---'
































































# --- NEW HELPER: Identify Scripture Match Types (Unchanged) ---
TORAH_BOOKS = {"Gen", "Exo", "Lev", "Num", "Deu"} # Abbreviations used in scripture_db
def check_scripture_match_type(db: dict, number: int) -> list:
    match_types = []
    is_bible = False
    is_torah = False
































































    # Check Bible/Torah
    if number in db['chapters'] or number in db['verses']:
        is_bible = True
        match_types.append("Bible")
        # Get the specific books that match this number
        books = db['chapters'].get(number, set()) | db['verses'].get(number, set())
        # Check if any of these books are Torah books
        if any(book_abbr in TORAH_BOOKS for book_abbr in books):
            is_torah = True
            match_types.append("Torah")
































































    # Check Quran
    if number in db['surahs'] or number in db['ayahs']:
        match_types.append("Quran")
































































    return match_types
































































# ------------------------
# Core Calculation & Analysis Functions (Unchanged)
# ------------------------
def build_concordance(phrases: list):
    concordance = defaultdict(list)
    total_phrases = len(phrases)
    print(f"Building concordance for {total_phrases} phrases...")
    # Progress indicator can be added here if needed
    for i, phrase in enumerate(phrases):
        s_clean = keep_letters_upper(phrase)
        if not s_clean: continue
        for cipher_name, cipher_fn in CIPHERS:
            try:
                value = int(cipher_fn(s_clean))
                concordance[(cipher_name, value)].append(phrase)
            except Exception as e:
                print(f"Error calculating cipher '{cipher_name}' for phrase '{phrase}': {e}")
    print("Concordance build complete.")
    return concordance
































































def perform_all_calculations(phrases: list):
    all_calculations = []
    total_expected = len(phrases) * len(CIPHERS)
    print(f"Performing all {total_expected} calculations for Grand Total Sum...")
    start_time = time.time()
    for i, phrase in enumerate(phrases):
        s_clean = keep_letters_upper(phrase)
        if not s_clean: continue
        for cipher_name, cipher_fn in CIPHERS:
            try:
                value = int(cipher_fn(s_clean))
                all_calculations.append({'phrase': phrase, 'cipher': cipher_name, 'value': value, 'clean': s_clean})
            except Exception as e:
                print(f"Error in Grand Total calc for '{cipher_name}' / '{phrase}': {e}")
        # Optional progress for this step
        # if (i + 1) % 50 == 0: print(f"  Calculated for {i+1}/{len(phrases)} phrases...")
    end_time = time.time()
    print(f"Finished all calculations in {end_time - start_time:.2f} seconds.")
    return all_calculations
































































def calculate_grand_total_unified(all_calculations: list, strongs_db: set, scripture_db: dict):
    print("Calculating Grand Total Sum (All Instances)...")
    start_time = time.time()
    grand_total = 0
    cross_cipher_instance_count = 0
    strongs_instance_count = 0
    bible_instance_count = 0
    torah_instance_count = 0
    quran_instance_count = 0
































































    # 1. Identify cross-cipher links
    phrase_to_values = defaultdict(lambda: defaultdict(list))
    for calc in all_calculations:
        phrase_to_values[calc['phrase']][calc['value']].append(calc['cipher'])
    cross_linked_tuples = set()
    for phrase, values_map in phrase_to_values.items():
        for value, ciphers in values_map.items():
            if len(ciphers) > 1:
                cross_linked_tuples.add((phrase, value))
































































    # 2. Iterate through all calculations and sum match instances
    for calc in all_calculations:
        value = calc['value']
        phrase = calc['phrase']
































































        # Check cross-cipher link
        if (phrase, value) in cross_linked_tuples:
            grand_total += 1
            cross_cipher_instance_count += 1
































































        # Check Strongs
        if get_strongs_match(strongs_db, value) != '---':
            grand_total += 1
            strongs_instance_count += 1
































































        # Check Scripture Types using the helper
        scripture_types = check_scripture_match_type(scripture_db, value)
































































        # Add +1 for a Bible match (and check for Torah subset)
        if "Bible" in scripture_types:
            grand_total += 1  # Add to grand total
            bible_instance_count += 1
            if "Torah" in scripture_types:
                torah_instance_count += 1
































































        # Add +1 for a Quran match
        if "Quran" in scripture_types:
            grand_total += 1  # Add to grand total
            quran_instance_count += 1
































































    end_time = time.time()
    print(f"Grand Total calculation finished in {end_time - start_time:.2f} seconds.")
































































    # Store breakdown for returning
    breakdown = {
        "cross_cipher": cross_cipher_instance_count,
        "strongs": strongs_instance_count,
        "bible": bible_instance_count,
        "torah": torah_instance_count,
        "quran": quran_instance_count
    }
































































    # Print the breakdown immediately
    print(f"  Grand Total Sum (All Instances): {grand_total}")
    print(f"  Breakdown:")
    print(f"    - Cross-Cipher Instances     : {breakdown['cross_cipher']}")
    print(f"    - Strongs Instances          : {breakdown['strongs']}")
    print(f"    - Bible Scripture Instances  : {breakdown['bible']}")
    print(f"      - Torah Subset Instances : {breakdown['torah']} (included in Bible total)")
    print(f"    - Quran Scripture Instances  : {breakdown['quran']}")
































































    return grand_total, breakdown
































































def build_phrase_value_map(concordance: dict):
    phrase_to_values = defaultdict(lambda: defaultdict(list))
    for (cipher, value), phrases in concordance.items():
        for phrase in phrases:
            phrase_to_values[phrase][value].append(cipher)
    return phrase_to_values
































































def identify_cross_cipher_hits(phrase_to_values: dict):
    cross_cipher_hits = set() # Store tuples of (cipher, value, phrase)
    for phrase, values_map in phrase_to_values.items():
        for value, ciphers in values_map.items():
            if len(ciphers) > 1:
                for cipher in ciphers:
                    cross_cipher_hits.add((cipher, value, phrase))
    print(f"Identified {len(cross_cipher_hits)} specific (Cipher, Value, Phrase) tuples involved in cross-cipher links for export logic.")
    return cross_cipher_hits
































































def export_connections(concordance: dict, cross_cipher_hits: set, out_csv: str, strongs_db: set, scripture_db: dict, strongs_map: dict, show_matches: bool=False):
    connections = []
    print("Finding and formatting connections for CSV (unified definition)...")
    for (cipher, value), phrases in concordance.items():
        strongs_match = get_strongs_match(strongs_db, value)
        scripture_match = get_scripture_match_compact(scripture_db, value)
        is_orig_significant = (len(phrases) > 1) or (strongs_match != '---') or (scripture_match != '---')
        is_cross_significant = any((cipher, value, p) in cross_cipher_hits for p in phrases)
































































        if is_orig_significant or is_cross_significant:
            formatted_detail = ""
            if show_matches: formatted_detail = format_strongs_and_scripture(value, strongs_map)
            connections.append({'Cipher': cipher, 'Value': value, 'Count': len(phrases), 'Strongs_Match': strongs_match, 'Scripture_Match': scripture_match, 'Connected Phrases': ' | '.join(phrases)})
            if show_matches:
                indicator = " (Cross-Cipher Link)" if is_cross_significant and not is_orig_significant else ""
                print(f"[Match]{indicator} Cipher={cipher:<18} | {formatted_detail}")
                joined_phrases = ' | '.join('"{}"'.format(ph) for ph in phrases)
                print(f"        Phrases ({len(phrases)}): {joined_phrases}\n")
































































    if not connections: print('No significant connections found for CSV.'); return 0
    connections.sort(key=lambda x: (-x['Count'], x['Value'], x['Cipher']))
    print(f"Found {len(connections)} significant connection groups for CSV (unified definition). Exporting to {out_csv}...")
    fieldnames = ['Cipher', 'Value', 'Count', 'Strongs_Match', 'Scripture_Match', 'Connected Phrases']
    try:
        with open(out_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames); writer.writeheader(); writer.writerows(connections)
        print(f"Successfully exported to {out_csv}")
    except Exception as e: print(f"Error writing to CSV: {e}"); return 0
    return len(connections)
































































def analyze_single_phrase(phrase: str, strongs_db: set, scripture_db: dict, strongs_map: dict):
    s_clean = keep_letters_upper(phrase)
    if not s_clean: print(f"Phrase '{phrase}' contains no calculable letters (A-Z)."); return
































































    print(f"\n--- Analyzing Single Phrase: '{phrase}' (Cleaned: '{s_clean}') ---")
    header_parts = ["Cipher", "Value", "Strongs", "Scripture", "Formatted Strongs/Scripture Match"]
    cipher_width = max(len(name) for name, _ in CIPHERS) + 2; value_width = 8; strongs_width = 15; scripture_width = 12
    header = f"{header_parts[0]:<{cipher_width}} | {header_parts[1]:<{value_width}} | {header_parts[2]:<{strongs_width}} | {header_parts[3]:<{scripture_width}} | {header_parts[4]}"
    separator = '-' * (len(header) + 40); print(separator); print(header); print(separator)
































































    results = []; value_to_ciphers = defaultdict(list)
    for cipher_name, cipher_fn in CIPHERS:
        try:
            value = int(cipher_fn(s_clean)); fmt = format_strongs_and_scripture(value, strongs_map)
            strongs_match = get_strongs_match(strongs_db, value); scripture_match = get_scripture_match_compact(scripture_db, value)
            formatted_line_data = {"cipher": cipher_name, "value": value, "strongs": strongs_match, "scripture": scripture_match, "formatted": fmt.split(' > ', 1)[1]}
            results.append(formatted_line_data); value_to_ciphers[value].append(cipher_name)
        except Exception as e:
             print(f"Error calculating cipher '{cipher_name}': {e}"); results.append({"cipher": cipher_name, "value": "Error", "strongs": "---", "scripture": "---", "formatted": f"Calc Error: {e}"})
































































    for res in results: print(f"{res['cipher']:<{cipher_width}} | {str(res['value']):<{value_width}} | {res['strongs']:<{strongs_width}} | {res['scripture']:<{scripture_width}} | {res['formatted']}")
    print(separator)
































































    print("\n--- Cross-Cipher Connection Report ---"); print(f"Analysis for: '{phrase}'")
    cross_cipher_matches = {v: c for v, c in value_to_ciphers.items() if len(c) > 1}
    if not cross_cipher_matches: print("No cross-cipher connections found."); print(separator); return
    sorted_matches = sorted(cross_cipher_matches.items(), key=lambda item: (-len(item[1]), item[0]))
    for value, ciphers in sorted_matches:
        detail_line = format_strongs_and_scripture(value, strongs_map).split(' > ', 1)[1];
        print(f"\n[Value: {value}] found {len(ciphers)} times. (Details: {detail_line})")
        for cipher_name in sorted(ciphers): print(f"  - {cipher_name}")
    print(separator)
































































# -----------------------------------------------------------------
# --- NEW FUNCTION: Granular Analysis of CSV Output ---
# -----------------------------------------------------------------
def perform_granular_analysis(csv_filepath: str):
    """
    Reads the exported CSV file and performs a granular analysis
    to identify the "Top Drivers" of the connections.
    """
    print("\n\n--- Granular Analysis of Exported CSV ---")
    print(f"Analyzing file: {csv_filepath}")
































































    try:
        # Set low_memory=False to help with potential mixed types
        df = pd.read_csv(csv_filepath, low_memory=False)
        if df.empty:
            print("CSV file is empty. No granular analysis to perform.")
            return
































































        print(f"Loaded {len(df)} significant connection groups for analysis.")
































































        # --- Analysis 1: Top 40 Phrases (by appearance in connection groups) ---
        print("\n--- [Analysis 1: Top 40 Most Connected Phrases (Overall)] ---")
        all_phrases = df['Connected Phrases'].astype(str).str.split(' | ').explode().str.strip()
        top_phrases = all_phrases.value_counts()
        print(top_phrases.head(40).to_string())
































































        # --- Analysis 2: Top 40 Values (by number of ciphers they connect) ---
        print("\n--- [Analysis 2: Top 40 Most Common Values (Across Ciphers)] ---")
        top_values = df['Value'].value_counts()
        print(top_values.head(40).to_string())
































































        # --- Analysis 3: Top 40 Connection Groups (by phrase count) ---
        print("\n--- [Analysis 3: Top 40 Largest Connection Groups (Most phrases for one value)] ---")
        df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
        top_groups = df.sort_values(by='Count', ascending=False)
        print(top_groups.head(40).to_string(
            columns=['Value', 'Cipher', 'Count', 'Strongs_Match', 'Scripture_Match'],
            index=False
        ))
































































        # --- Analysis 4: Top 40 Phrases driving Strong's Hits ---
        print("\n--- [Analysis 4: Top 40 Phrases Driving Strong's Concordance Hits] ---")
        strongs_df = df[df['Strongs_Match'].astype(str) != '---'].copy()
        if strongs_df.empty:
            print("No Strong's matches found in CSV.")
        else:
            strongs_phrases = strongs_df['Connected Phrases'].astype(str).str.split(' | ').explode().str.strip()
            top_strongs_phrases = strongs_phrases.value_counts()
            print(top_strongs_phrases.head(40).to_string())
































































        # --- Analysis 5: Top 40 Phrases driving Scripture Hits ---
        print("\n--- [Analysis 5: Top 40 Phrases Driving Scripture (Bible/Quran) Hits] ---")
        scripture_df = df[df['Scripture_Match'].astype(str) != '---'].copy()
        if scripture_df.empty:
            print("No Scripture matches found in CSV.")
        else:
            scripture_phrases = scripture_df['Connected Phrases'].astype(str).str.split(' | ').explode().str.strip()
            top_scripture_phrases = scripture_phrases.value_counts()
            print(top_scripture_phrases.head(40).to_string())
































































        print("\n--- Granular Analysis Complete ---")
































































    except FileNotFoundError:
        print(f"*** ERROR: Could not find CSV file for analysis: {csv_filepath}")
    except Exception as e:
        print(f"*** ERROR during granular analysis: {e}")
        # Add more specific check for pandas import error
        if isinstance(e, ModuleNotFoundError) and 'pandas' in str(e):
             print("*** It seems pandas might not be installed correctly or Pydroid needs a restart.")
             print("    Please try restarting Pydroid fully and running the script again.")
        else:
            print("    Please ensure pandas is installed correctly ('pip install pandas') and try again.")
































































# -----------------------------------------------------
# --- MODIFIED main() function to call new analysis ---
# -----------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description='ANI Concordance Constellation Engine v3.9.5 — Detailed Breakdown & Analysis')
    ap.add_argument('--export', default=DEFAULT_OUT, help=f'Output CSV path (default: {DEFAULT_OUT})')
    ap.add_argument('--phrase', type=str, help='Analyze a single phrase instead of the full concordance')
    ap.add_argument('--show-matches', action='store_true', help='Print connection details live to console during full analysis')
    ap.add_argument('--strongs-xlsx', type=str, help="Optional path to Strong's Excel file (.xlsx) to load full mappings.")
    args = ap.parse_args()
































































    print("Initializing databases...")
    strongs_db = create_strongs_db()
    scripture_db = create_scripture_db()
































































    strongs_map = BUILTIN_STRONGS.copy()
    if args.strongs_xlsx:
        excel_map = load_strongs_from_excel(args.strongs_xlsx)
        if excel_map:
            strongs_map.update(excel_map)
            print(f"Excel data loaded. Total Strong's definitions available: {len(strongs_map)}")
        else:
            print("Excel loading failed. Using built-in Strong's only.")
    else:
        print("No Strong's Excel file specified. Using built-in definitions only.")
        print(f"Total Strong's definitions available: {len(strongs_map)}")
































































    # --- Perform ALL calculations first for the Grand Total & Breakdown ---
    # Use the updated PHRASES list
    all_calculations = perform_all_calculations(PHRASES)
    grand_total_sum, grand_total_breakdown = calculate_grand_total_unified(all_calculations, strongs_db, scripture_db)
































































    # --- Mode Selection ---
    total_csv_connections = 0 # Initialize here
    csv_path_display = "N/A" # Initialize here
































































    if args.phrase:
        # Single Phrase Mode still only analyzes one phrase for its detailed report
        analyze_single_phrase(args.phrase, strongs_db, scripture_db, strongs_map)
        mode_description = "Single Phrase Analysis"
        total_csv_connections_display = "N/A (Single Phrase Mode)" # Display N/A for CSV count
    else:
        # Full Concordance Mode uses the pre-calculated results to build concordance
        mode_description = "Full Concordance"
        print("Building concordance from all calculations...")
        concordance = defaultdict(list)
        for calc in all_calculations:
             concordance[(calc['cipher'], calc['value'])].append(calc['phrase'])
        print("Concordance build complete.")
































































        phrase_value_map = build_phrase_value_map(concordance)
        cross_cipher_hits_set = identify_cross_cipher_hits(phrase_value_map)
































































        total_csv_connections = export_connections( # Assign the return value
            concordance, cross_cipher_hits_set, args.export,
            strongs_db, scripture_db, strongs_map, args.show_matches
        )
        total_csv_connections_display = total_csv_connections # Use the actual count
































































        if total_csv_connections > 0:
            # --- THIS IS THE NEW PART ---
            # Get the *actual* full path of the exported file
            resolved_csv_path = str(Path(args.export).resolve())
            csv_path_display = resolved_csv_path
            # Call the new analysis function on the file we just created
            perform_granular_analysis(resolved_csv_path)
            # --- END OF NEW PART ---
        else:
            csv_path_display = "N/A (No connections found)"
































































    # --- Final On-Screen Output (Unchanged) ---
    print("\n\n--- Analysis Summary ---")
    print(f"Mode: {mode_description}")
    # Update total scanned phrases count
    print(f"Total Scanned phrases: {len(PHRASES)}")
    print(f"Total Calculations Performed: {len(all_calculations)}")
    print("-" * 45) # Separator
    print(f"Grand Total Scanned All Instances: {grand_total_sum}")
    print(f"Connections Groups Exported To CSV Total Sum: {total_csv_connections_display}")
    print("-" * 45) # Separator
    print(f"Cross Ciphers w/Hindi / Hindu/ Buddhist Connections: {grand_total_breakdown['cross_cipher']}")
    print(f"Hebrew/Greek Strong Concordances Matches/ Connections: {grand_total_breakdown['strongs']}")
    print(f"Biblical Scriptures Matches/ Connections: {grand_total_breakdown['bible']}")
    print(f"  Torah Matches/ Connections (Subset of Biblical): {grand_total_breakdown['torah']}")
    print(f"Quran Matches/ Connections: {grand_total_breakdown['quran']}")
    print("-" * 45) # Separator
    # Keep the labels as requested, even if numbers repeat meaning
    print(f"Total Scanned (All Instances): {grand_total_sum}") # Repeating Grand Total
    print(f"Total Matches / Connections Grand Sum (CSV Groups): {total_csv_connections_display}")
    print(f"Grand Total Connections And Matches (All Instances): {grand_total_sum}") # Repeating Grand Total
    print(f"CSV Output Path: {csv_path_display}")
    print("-" * 45) # Separator
    print("\n[Program finished]")
# --- END OF main() function ---
































































if __name__ == '__main__':
    try:
        main()
    except Exception as e:
         print(f"\n--- An unexpected error occurred ---")
         print(f"Error Type: {type(e).__name__}")
         print(f"Error Details: {e}")
         # import traceback; traceback.print_exc() # Uncomment for debugging
         # Add a specific check for ModuleNotFoundError related to pandas
         if isinstance(e, ModuleNotFoundError) and 'pandas' in str(e):
             print("*** It seems pandas might not be installed correctly or Pydroid needs a restart.")
             print("    Please try restarting Pydroid fully and running the script again.")
         sys.exit(1)