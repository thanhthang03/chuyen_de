from PyQt6 import QtCore, QtGui, QtWidgets
import resAI
import pyodbc
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# (thang) library for record and save buttons
import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import os

# (thang) library for A.I summarize button
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
import re

#(duc) library for convertToText button
import speech_recognition as sr
import pydub 