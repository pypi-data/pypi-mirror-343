# Copyright 2024 Mario Graff (https://github.com/mgraffg)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from dataclasses import dataclass
from os.path import isfile
import os
import numpy as np
from encexp.download import download_seqtm, download_encexp, main, download_TextModel


def test_download_seqtm():
    """Test download seqtm vocabulary"""
    data = download_seqtm(lang='es', output='t.json.gz')
    assert isfile('t.json.gz')
    os.unlink('t.json.gz')
    assert len(data['counter']['dict']) == 2**13
    download_seqtm(lang='es')


def test_download_encexp():
    """Test download EncExp"""

    data = download_encexp(lang='es', voc_source='mix',
                           enc_source=None,
                           precision=np.float16)
    dim = 2**13
    # assert list(data.keys()) is None
    assert len(data['seqtm']['counter']['dict']) == dim
    assert len(data['coefs'])
    for coef in data['coefs']:
        assert coef['coef'].shape[0] == dim
        assert coef['coef'].dtype == np.float16


def test_download_main():
    """Test download main"""
    @dataclass
    class A:
        voc_size_exponent = 13
        lang = 'es'
        output = None
        voc_source = 'noGeo'
        enc_source = None
        seqtm = False
        encexp = True
        prefix_suffix = True
        
    args = A()
    main(args)


def test_download_TextModel():
    """Test download TextModel"""
    from encexp import TextModel
    tm = TextModel(lang='ca')
    download_TextModel(tm.identifier)