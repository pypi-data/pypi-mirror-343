#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                   $Date$
#                   $Author$
#
#  Copyright (c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#   DESCRIPTION
#
#  This file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
import os
import sys
import traceback
from gurux_serial import GXSerial
from gurux_net import GXNet
from gurux_dlms.enums import ObjectType
from gurux_dlms.objects.GXDLMSObjectCollection import GXDLMSObjectCollection
from .GXSettings import GXSettings
from .GXDLMSReader import GXDLMSReader
from gurux_dlms.GXDLMSClient import GXDLMSClient
from gurux_common.GXCommon import GXCommon
from gurux_dlms.enums.DataType import DataType
import locale
from gurux_dlms.GXDateTime import GXDateTime
from gurux_dlms.internal._GXCommon import _GXCommon
from gurux_dlms import GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError, GXDLMSTranslator
from gurux_dlms import GXByteBuffer, GXDLMSTranslatorMessage, GXReplyData
from gurux_dlms.enums import RequestTypes, Security, InterfaceType
from gurux_dlms.secure.GXDLMSSecureClient import GXDLMSSecureClient


#pylint: disable=too-few-public-methods,broad-except
class DummyObject:
    def __init__(self, name, objectType):
        self.name = name
        self.objectType = objectType

class DlmsAgent():
    def __init__(self):
        self.reader = None
        self.settings = GXSettings()
        self.settings.media = GXNet()
        self.settings.media.hostName = "localhost"  # Default host
        self.settings.media.port = 4059  # Default DLMS/COSEM port
        self.settings.client.clientAddress = 16
        self.settings.client.serverAddress = 1
        self.settings.client.authentication = 0
        self.settings.client.useLogicalNameReferencing = True

        #self.connargs = "-S COM10:115200:8None1 -a None -c 16 -s 1 -r ln"

    def connect(self):
        try:
            # //////////////////////////////////////
            #  Initialize connection self.settings.
            if not isinstance(self.settings.media, (GXSerial, GXNet)):
                raise Exception("Unknown media type.")
            # //////////////////////////////////////

            self.reader = GXDLMSReader(self.settings.client, self.settings.media, self.settings.trace, self.settings.invocationCounter)

            self.settings.media.open()
            if self.settings.readObjects:
                read = False
                self.reader.initializeConnection()
                if self.settings.outputFile and os.path.exists(self.settings.outputFile):
                    try:
                        c = GXDLMSObjectCollection.load(self.settings.outputFile)
                        self.settings.client.objects.extend(c)
                        if self.settings.client.objects:
                            read = True
                    except Exception:
                        read = False
                if not read:
                    self.reader.getAssociationView()
                if self.settings.outputFile:
                    self.settings.client.objects.save(self.settings.outputFile)
            else:
                self.reader.readAll(self.settings.outputFile)

        except (ValueError, GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError) as ex:
            print(ex)
        except (KeyboardInterrupt, SystemExit, Exception) as ex:
            traceback.print_exc()
            if self.settings.media:
                self.settings.media.close()
            self.reader = None
        #finally:
        #    try:
        #        self.reader.close()
        #    except Exception:
        #        traceback.print_exc()
        
    def readObject(self, args) -> str:
        try:
            tmp = args.split(":")
            if len(tmp) != 3:
                raise ValueError("Invalid Logical name or attribute index.")

            j = tmp[0].strip()
            k = tmp[1].strip()
            v = tmp[2].strip()

            obj = self.settings.client.objects.findByLN(ObjectType.NONE, k)
            if obj is None:
                obj = _GXObjectFactory.createObject(j, ObjectType(j))
                self.settings.client.objects.append(obj)
            val = self.reader.read(obj, int(v))
            return val

        except (ValueError, GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError) as ex:
            print(ex)
        except (KeyboardInterrupt, SystemExit, Exception) as ex:
            traceback.print_exc()
            if self.settings.media:
                self.settings.media.close()
            self.reader = None
        finally:
            print("Read Complete")

    def writeObject(self, args, value) -> bool:
        """Write value to object with error handling"""
        try:
            tmp = args.split(":")
            if len(tmp) != 3:
                raise ValueError("Invalid Logical name or attribute index.")

            j = tmp[0].strip()
            k = tmp[1].strip()
            v = tmp[2].strip()

            obj = self.settings.client.objects.findByLN(ObjectType.NONE, k)
            if obj is None:
                obj = _GXObjectFactory.createObject(j, ObjectType(j))
                self.settings.client.objects.append(obj)
            obj.value = value
            self.reader.write(obj, int(v))
            return True

        except (ValueError, GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError) as ex:
            print(ex)
        except (KeyboardInterrupt, SystemExit, Exception) as ex:
            traceback.print_exc()
            if self.settings.media:
                self.settings.media.close()
            self.reader = None
        finally:
            print("Write Complete")

    def disconnect(self):
        if self.reader:
            try:
                self.reader.close()
            except Exception:
                traceback.print_exc()