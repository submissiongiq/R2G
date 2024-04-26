#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from bertopic import BERTopic
import matplotlib.pyplot as plt

# Where the key is topics, this model has 267 clusters.
topic_mapping = {-1: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 0: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Information Requests'}, 1: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 2: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Insurance'}, 3: {'cluster_id': 2, 'cluster_name': 'Pet', 'sub_cluster': 'Pet'}, 4: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Asylum'}, 5: {'cluster_id': 3, 'cluster_name': 'Transportation', 'sub_cluster': 'Ticket Inquiries'}, 6: {'cluster_id': 3, 'cluster_name': 'Transportation', 'sub_cluster': 'Carriers, Transport to and from Ukraine'}, 7: {'cluster_id': 4, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 8: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 9: {'cluster_id': 5, 'cluster_name': 'Volunteering', 'sub_cluster': 'Volunteering'}, 10: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Communication'}, 11: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Translation Services'}, 12: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Passport'}, 13: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Dentistry'}, 14: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Job'}, 15: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Currency'}, 16: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Banking'}, 17: {'cluster_id': 8, 'cluster_name': 'Social Services', 'sub_cluster': 'Protocols'}, 18: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Mail'}, 19: {'cluster_id': 9, 'cluster_name': 'Education', 'sub_cluster': 'Education'}, 20: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Clothing'}, 21: {'cluster_id': 8, 'cluster_name': 'Social Services', 'sub_cluster': 'Financial Assistance'}, 22: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 23: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 24: {'cluster_id': 3, 'cluster_name': 'Transportation', 'sub_cluster': 'Carriers, Transport to and from Ukraine'}, 25: {'cluster_id': 9, 'cluster_name': 'Education', 'sub_cluster': 'Education'}, 26: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 27: {'cluster_id': 3, 'cluster_name': 'Transportation', 'sub_cluster': 'Public Transportation'}, 28: {'cluster_id': 4, 'cluster_name': 'Accommodation', 'sub_cluster': 'Leasing Regulation'}, 29: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 30: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Open Chat'}, 31: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Communication'}, 32: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 33: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Regulation'}, 34: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Food'}, 35: {'cluster_id': 2, 'cluster_name': 'Pet', 'sub_cluster': 'Pet'}, 36: {'cluster_id': 3, 'cluster_name': 'Transportation', 'sub_cluster': 'Carriers, Transport to and from Ukraine'}, 37: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Vehicle'}, 38: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 39: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 40: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Request'}, 41: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 42: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Status Acquisition'}, 43: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Consulate Services'}, 44: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 45: {'cluster_id': 3, 'cluster_name': 'Transportation', 'sub_cluster': 'Public Transportation'}, 46: {'cluster_id': 5, 'cluster_name': 'Volunteering', 'sub_cluster': 'Volunteering'}, 47: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 48: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Vehicle'}, 49: {'cluster_id': 4, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 50: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 51: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'War Chat'}, 52: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 53: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Network Provider'}, 54: {'cluster_id': 9, 'cluster_name': 'Education', 'sub_cluster': 'Education'}, 55: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 56: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 57: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Asylum'}, 58: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 59: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 60: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Tax'}, 61: {'cluster_id': 4, 'cluster_name': 'Accommodation', 'sub_cluster': 'Expense'}, 62: {'cluster_id': 4, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 63: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 64: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 65: {'cluster_id': 3, 'cluster_name': 'Transportation', 'sub_cluster': 'Carriers, Transport to and from Ukraine'}, 66: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 67: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 68: {'cluster_id': 3, 'cluster_name': 'Transportation', 'sub_cluster': 'Public Transportation'}, 69: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Family Reunion'}, 70: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 71: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Request'}, 72: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 73: {'cluster_id': 3, 'cluster_name': 'Transportation', 'sub_cluster': 'Public Transportation'}, 74: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 75: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Vaccinations'}, 76: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Police'}, 77: {'cluster_id': 8, 'cluster_name': 'Social Services', 'sub_cluster': 'Financial Assistance'}, 78: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Regulation'}, 79: {'cluster_id': 3, 'cluster_name': 'Transportation', 'sub_cluster': 'Carriers, Transport to and from Ukraine'}, 80: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 81: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Request'}, 82: {'cluster_id': 3, 'cluster_name': 'Transportation', 'sub_cluster': 'Public Transportation'}, 83: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Parking'}, 84: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 85: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 86: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 87: {'cluster_id': 11, 'cluster_name': 'Legal information', 'sub_cluster': 'Legal information'}, 88: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 89: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 90: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Insurance'}, 91: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Network Provider'}, 92: {'cluster_id': 9, 'cluster_name': 'Education', 'sub_cluster': 'Education'}, 93: {'cluster_id': 4, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 94: {'cluster_id': 12, 'cluster_name': 'Religious Information', 'sub_cluster': 'Religious Information'}, 95: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Network Provider'}, 96: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 97: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 98: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 99: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 100: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Banking'}, 101: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 102: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 103: {'cluster_id': 8, 'cluster_name': 'Social Services', 'sub_cluster': 'Library'}, 104: {'cluster_id': 8, 'cluster_name': 'Social Services', 'sub_cluster': 'Library'}, 105: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Tax'}, 106: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Police'}, 107: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 108: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 109: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Network Provider'}, 110: {'cluster_id': 11, 'cluster_name': 'Legal information', 'sub_cluster': 'Legal information'}, 111: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Passport'}, 112: {'cluster_id': 9, 'cluster_name': 'Education', 'sub_cluster': 'Education'}, 113: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Regulation'}, 114: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 115: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 116: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 117: {'cluster_id': 9, 'cluster_name': 'Education', 'sub_cluster': 'Education'}, 118: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Job'}, 119: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 120: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 121: {'cluster_id': 4, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 122: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Translation Services'}, 123: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Insurance'}, 124: {'cluster_id': 4, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 125: {'cluster_id': 11, 'cluster_name': 'Legal information', 'sub_cluster': 'Legal information'}, 126: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 127: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 128: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 129: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Psychotherapy'}, 130: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 131: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 132: {'cluster_id': 4, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 133: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 134: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 135: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Home Appliances'}, 136: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 137: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 138: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 139: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Tax'}, 140: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Vaccinations'}, 141: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 142: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Request'}, 143: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 144: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 145: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 146: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 147: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Job'}, 148: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Vehicle'}, 149: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 150: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 151: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 152: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Request'}, 153: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 154: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 155: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 156: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 157: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 158: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 159: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 160: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Communication'}, 161: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 162: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 163: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 164: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 165: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 166: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 167: {'cluster_id': 3, 'cluster_name': 'Transportation', 'sub_cluster': 'Public Transportation'}, 168: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Communication'}, 169: {'cluster_id': 12, 'cluster_name': 'Religious Information', 'sub_cluster': 'Religious Information'}, 170: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 171: {'cluster_id': 3, 'cluster_name': 'Transportation', 'sub_cluster': 'Taxi Services'}, 172: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 173: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 174: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 175: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Open Chat'}, 176: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 177: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 178: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 179: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 180: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 181: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 182: {'cluster_id': 11, 'cluster_name': 'Legal information', 'sub_cluster': 'Divorce'}, 183: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 184: {'cluster_id': 8, 'cluster_name': 'Social Services', 'sub_cluster': 'Protocols'}, 185: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 186: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 187: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 188: {'cluster_id': 11, 'cluster_name': 'Legal information', 'sub_cluster': 'Marriage'}, 189: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Job'}, 190: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 191: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 192: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 193: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 194: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 195: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 196: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 197: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 198: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 199: {'cluster_id': 5, 'cluster_name': 'Volunteering', 'sub_cluster': 'Volunteering'}, 200: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Job'}, 201: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Logistics'}, 202: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 203: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Consulate Services'}, 204: {'cluster_id': 4, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 205: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 206: {'cluster_id': 4, 'cluster_name': 'Accommodation', 'sub_cluster': 'Leasing Regulation'}, 207: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 208: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Job'}, 209: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 210: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 211: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 212: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 213: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Infant & Toddler Care'}, 214: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 215: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 216: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 217: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Regulation'}, 218: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 219: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Request'}, 220: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 221: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 222: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Hospice Care'}, 223: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 224: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 225: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Request'}, 226: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 227: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Dentistry'}, 228: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 229: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 230: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Customs'}, 231: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 232: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 233: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Customs'}, 234: {'cluster_id': 6, 'cluster_name': 'Integration', 'sub_cluster': 'Customs'}, 235: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Disability'}, 236: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 237: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 238: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 239: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 240: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Regulation'}, 241: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Network Provider'}, 242: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 243: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 244: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 245: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 246: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 247: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 248: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 249: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 250: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 251: {'cluster_id': 10, 'cluster_name': 'Social Activity', 'sub_cluster': 'Regulation'}, 252: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 253: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Open Chat'}, 254: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 255: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Request'}, 256: {'cluster_id': 0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 257: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 258: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 259: {'cluster_id': 8, 'cluster_name': 'Social Services', 'sub_cluster': 'Protocols'}, 260: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 261: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 262: {'cluster_id': -1, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 263: {'cluster_id': 1, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Infant & Toddler Care'}, 264: {'cluster_id': 7, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 265: {'cluster_id': 5, 'cluster_name': 'Volunteering', 'sub_cluster': 'Volunteering'}}
## Load your test data excluding the first 100,000 rows, rest of data as validation set, need to redefine the path.
df = pd.read_csv("/content/df_telegram_test.csv", skiprows=range(1, 100001), encoding='utf-8')

# Load huggingface model and predict
topic_model = BERTopic.load("Alprocco/Bert_Ukr_in_Swiss")
topics, _ = topic_model.transform(df['text'])
df['topic_id_fit'] = topics

# Use the 'topic_id_fit' column to map to the cluster ID, name, and sub-cluster
df['cluster_id_fit'] = df['topic_id_fit'].map(lambda x: topic_mapping[x]['cluster_id'])
df['cluster_name_fit'] = df['topic_id_fit'].map(lambda x: topic_mapping[x]['cluster_name'])
df['sub_cluster'] = df['topic_id_fit'].map(lambda x: topic_mapping[x]['sub_cluster'])

df.to_csv("/content/df_telegram_test_fit.csv", index=False, encoding='utf-8')

# Read attribute
print(df.columns)

# After mapping, validate the label with the supervised dataset by mapping the top three old clusters for each new subcluster.
# Group by 'sub_cluster' and 'cluster_name' and get the size of each group
grouped = df.groupby(['sub_cluster', 'cluster_name']).size().reset_index(name='count')

# Sort the values and get the top 3 'cluster_name' for each 'sub_cluster'
top3 = grouped.groupby('sub_cluster').apply(lambda x: x.nlargest(3, 'count')).reset_index(drop=True)

# Calculate the proportions
top3['proportion'] = top3.groupby('sub_cluster')['count'].apply(lambda x: x / x.sum())

# Print the results
print(top3)

# Save the top3 DataFrame to a .txt file
with open("/content/top3_clusters.txt", 'w', encoding='utf-8') as f:
    for _, row in top3.iterrows():
        f.write(f"Sub Cluster: {row['sub_cluster']}, Cluster Name: {row['cluster_name']}, Count: {row['count']}, Proportion: {row['proportion']:.2f}\n")

top3.to_csv("/content/top3_clusters.csv", index=False)